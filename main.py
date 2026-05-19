from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
import openpyxl
import io

from database import engine, get_db
from db_models import ProductORM, Base
from typing import List
from model import Product, ProductCreate, ProductUpdate, ProductPreviewRow, PreviewResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/getallproducts")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(ProductORM).all()


@app.get("/getproductbyid/{id}")
def get_product_by_id(id: UUID, db: Session = Depends(get_db)):
    product = db.query(ProductORM).filter(ProductORM.id == str(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/addproduct", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = ProductORM(
        id=str(uuid4()),
        name=product.name,
        description=product.description,
        price=product.price,
        is_active=product.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.delete("/deleteproduct/{id}")
def delete_product(id: UUID, db: Session = Depends(get_db)):
    product = db.query(ProductORM).filter(ProductORM.id == str(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product '{product.name}' deleted successfully"}


@app.get("/importtemplate")
def download_import_template():
    """Return a sample .xlsx file users can fill in and re-upload."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"

    # Header row
    headers = ["name", "description", "price", "is_active"]
    ws.append(headers)

    # Style header row bold
    from openpyxl.styles import Font, PatternFill, Alignment
    header_fill = PatternFill("solid", fgColor="4F46E5")
    for col_idx, _ in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    # Sample rows
    ws.append(["Wireless Headphones", "Noise-cancelling over-ear headphones", 3499.99, True])
    ws.append(["USB-C Hub 7-in-1",    "Multiport adapter for laptops",        1299.00, True])
    ws.append(["Laptop Stand",         "",                                      899.50, False])

    # Column widths
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 42
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 12

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=products_template.xlsx"},
    )


@app.post("/previewimport", response_model=PreviewResponse)
async def preview_import(file: UploadFile = File(...)):
    """Parse an Excel file and return rows with validation — no DB writes."""
    filename = file.filename or ""
    if not filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx and .xls files are supported.")

    contents = await file.read()
    try:
        wb = openpyxl.load_workbook(io.BytesIO(contents), data_only=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the file. Make sure it is a valid Excel workbook.")

    ws = wb.active
    raw_headers = [str(cell.value).strip().lower() if cell.value is not None else "" for cell in ws[1]]

    required_cols = {"name", "price"}
    missing = required_cols - set(raw_headers)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required column(s): {', '.join(sorted(missing))}. Please use the provided template.",
        )

    name_idx   = raw_headers.index("name")
    price_idx  = raw_headers.index("price")
    desc_idx   = raw_headers.index("description") if "description" in raw_headers else None
    active_idx = raw_headers.index("is_active")   if "is_active"   in raw_headers else None

    rows = []
    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if all(v is None or str(v).strip() == "" for v in row):
            continue

        raw_name = row[name_idx]
        name = str(raw_name).strip() if raw_name is not None else ""
        if not name or name.lower() == "none":
            rows.append(ProductPreviewRow(row_num=row_num, name="", valid=False, reason="Name is required and cannot be empty."))
            continue

        raw_price = row[price_idx]
        try:
            price = float(raw_price)
            if price <= 0:
                raise ValueError()
        except (TypeError, ValueError):
            rows.append(ProductPreviewRow(row_num=row_num, name=name, valid=False, reason=f"Invalid price '{raw_price}'. Must be a positive number."))
            continue

        description = None
        if desc_idx is not None:
            raw_desc = row[desc_idx]
            if raw_desc is not None and str(raw_desc).strip() not in ("", "None"):
                description = str(raw_desc).strip()

        is_active = True
        if active_idx is not None:
            raw_active = row[active_idx]
            if isinstance(raw_active, bool):
                is_active = raw_active
            elif raw_active is not None:
                is_active = str(raw_active).strip().lower() in ("true", "1", "yes", "active")

        rows.append(ProductPreviewRow(
            row_num=row_num, name=name, description=description,
            price=price, is_active=is_active, valid=True,
        ))

    valid_count = sum(1 for r in rows if r.valid)
    return PreviewResponse(total=len(rows), valid_count=valid_count, rows=rows)


@app.post("/importselected")
def import_selected(products: List[ProductCreate], db: Session = Depends(get_db)):
    """Insert a list of pre-validated products chosen by the user."""
    if not products:
        raise HTTPException(status_code=400, detail="No products provided.")
    for p in products:
        db.add(ProductORM(
            id=str(uuid4()),
            name=p.name,
            description=p.description,
            price=p.price,
            is_active=p.is_active,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ))
    db.commit()
    return {"imported": len(products)}


@app.post("/importproducts")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Bulk-import products from an uploaded .xlsx / .xls file."""
    filename = file.filename or ""
    if not filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx and .xls files are supported.")

    contents = await file.read()
    try:
        wb = openpyxl.load_workbook(io.BytesIO(contents), data_only=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the file. Make sure it is a valid Excel workbook.")

    ws = wb.active

    # Parse headers from row 1
    raw_headers = [str(cell.value).strip().lower() if cell.value is not None else "" for cell in ws[1]]

    required_cols = {"name", "price"}
    missing = required_cols - set(raw_headers)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required column(s): {', '.join(sorted(missing))}. "
                   f"Please use the provided template.",
        )

    name_idx  = raw_headers.index("name")
    price_idx = raw_headers.index("price")
    desc_idx  = raw_headers.index("description") if "description" in raw_headers else None
    active_idx = raw_headers.index("is_active")  if "is_active"   in raw_headers else None

    imported = 0
    errors   = []

    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        # Skip completely empty rows
        if all(v is None or str(v).strip() == "" for v in row):
            continue

        # --- name ---
        raw_name = row[name_idx]
        name = str(raw_name).strip() if raw_name is not None else ""
        if not name or name.lower() == "none":
            errors.append({"row": row_num, "name": "", "reason": "Name is required and cannot be empty."})
            continue

        # --- price ---
        raw_price = row[price_idx]
        try:
            price = float(raw_price)
            if price <= 0:
                raise ValueError("must be > 0")
        except (TypeError, ValueError):
            errors.append({"row": row_num, "name": name, "reason": f"Invalid price '{raw_price}'. Must be a positive number."})
            continue

        # --- description (optional) ---
        description = None
        if desc_idx is not None:
            raw_desc = row[desc_idx]
            if raw_desc is not None and str(raw_desc).strip() not in ("", "None"):
                description = str(raw_desc).strip()

        # --- is_active (optional, default True) ---
        is_active = True
        if active_idx is not None:
            raw_active = row[active_idx]
            if isinstance(raw_active, bool):
                is_active = raw_active
            elif raw_active is not None:
                is_active = str(raw_active).strip().lower() in ("true", "1", "yes", "active")

        try:
            db.add(ProductORM(
                id=str(uuid4()),
                name=name,
                description=description,
                price=price,
                is_active=is_active,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ))
            imported += 1
        except Exception as exc:
            errors.append({"row": row_num, "name": name, "reason": str(exc)})

    if imported:
        db.commit()

    return {"imported": imported, "skipped": len(errors), "errors": errors}


@app.put("/updateproduct/{id}", response_model=Product)
def update_product(id: UUID, data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(ProductORM).filter(ProductORM.id == str(id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.name is not None:
        product.name = data.name
    if data.description is not None:
        product.description = data.description
    if data.price is not None:
        product.price = data.price
    if data.is_active is not None:
        product.is_active = data.is_active

    product.updated_at = datetime.now()
    db.commit()
    db.refresh(product)
    return product



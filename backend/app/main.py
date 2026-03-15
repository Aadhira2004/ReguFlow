from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

class Device(BaseModel):
    name: str
    is_invasive: bool
    is_active: bool
    is_life_sustaining: bool
    contacts_cns_heart: bool
    is_sterile: bool

@app.post('/classify')
async def classify(device: Device):
    if device.contacts_cns_heart or device.is_life_sustaining:
        risk, rule = 'Class D', 'Rule 4(1)'
    elif device.is_invasive:
        risk, rule = 'Class C', 'Rule 4(2)'
    else:
        risk, rule = 'Class A', 'Rule 3'
    return {'analysis': {'device': device.name, 'class': risk, 'rule_applied': rule}, 'licensing': {'authority': 'Central (CLA)' if risk in ['Class C', 'Class D'] else 'State (SLA)'}, 'compliance_checklist': ['ISO 13485', 'Labeling', 'IFU']}

@app.get('/download-pdf')
async def download_pdf(name: str, risk: str):
    file_path = f'{name}_report.pdf'
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, f'ReguFlow Report for {name}')
    c.drawString(100, 730, f'Risk Category: {risk}')
    c.save()
    return FileResponse(file_path, filename=file_path)
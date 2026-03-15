from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This is the 'Master Key' for browser security
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class Device(BaseModel):
    name: str
    is_invasive: bool
    is_active: bool
    is_life_sustaining: bool
    contacts_cns_heart: bool
    is_sterile: bool

@app.post('/classify')
async def classify(device: Device):
    # CDSCO Logic
    if device.contacts_cns_heart or device.is_life_sustaining:
        risk, rule = 'Class D', 'Rule 4(1)'
    elif device.is_invasive:
        risk, rule = 'Class C', 'Rule 4(2)'
    elif device.is_active:
        risk, rule = 'Class B', 'Rule 3'
    else:
        risk, rule = 'Class A', 'Rule 3'
    
    return {
        'analysis': {'device': device.name, 'class': risk, 'rule_applied': rule},
        'licensing': {'authority': 'Central (CLA)' if risk in ['Class C', 'Class D'] else 'State (SLA)'},
        'compliance_checklist': ['ISO 13485', 'Labeling', 'IFU']
    }
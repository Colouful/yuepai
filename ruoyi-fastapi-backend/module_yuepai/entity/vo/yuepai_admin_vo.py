"""约拍管理后台VO"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CertReviewQuery(BaseModel):
    cert_type: Optional[str] = None
    status: Optional[str] = None
    real_name: Optional[str] = None
    page_num: int = 1
    page_size: int = 20

class CertReviewVO(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    cert_type: Optional[str] = None
    real_name: Optional[str] = None
    id_card: Optional[str] = None
    id_card_front: Optional[str] = None
    id_card_back: Optional[str] = None
    cert_images: Optional[list] = None
    description: Optional[str] = None
    status: Optional[str] = None
    reviewer: Optional[str] = None
    review_time: Optional[datetime] = None
    review_remark: Optional[str] = None
    create_time: Optional[datetime] = None
    class Config:
        from_attributes = True

class CertReviewAudit(BaseModel):
    id: int
    status: str = Field(..., description='1通过 2驳回')
    review_remark: Optional[str] = None


class AftersaleQuery(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    ticket_no: Optional[str] = None
    page_num: int = 1
    page_size: int = 20

class AftersaleVO(BaseModel):
    id: Optional[int] = None
    ticket_no: Optional[str] = None
    order_id: Optional[int] = None
    order_no: Optional[str] = None
    type: Optional[str] = None
    applicant_id: Optional[int] = None
    respondent_id: Optional[int] = None
    amount: Optional[float] = None
    reason: Optional[str] = None
    description: Optional[str] = None
    evidence: Optional[list] = None
    status: Optional[str] = None
    handler: Optional[str] = None
    handle_time: Optional[datetime] = None
    handle_result: Optional[str] = None
    create_time: Optional[datetime] = None
    class Config:
        from_attributes = True

class AftersaleHandle(BaseModel):
    id: int
    status: str
    handle_result: Optional[str] = None


class OperationQuery(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    page_num: int = 1
    page_size: int = 20

class OperationVO(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None
    config: Optional[dict] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None
    view_count: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    class Config:
        from_attributes = True

class OperationSave(BaseModel):
    id: Optional[int] = None
    type: str
    title: str
    content: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None
    config: Optional[dict] = None
    sort_order: int = 0
    status: str = '1'
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class RiskQuery(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    risk_level: Optional[str] = None
    page_num: int = 1
    page_size: int = 20

class RiskVO(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    target_name: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[int] = None
    reason: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    block_type: Optional[str] = None
    block_days: Optional[int] = None
    status: Optional[str] = None
    operator: Optional[str] = None
    operate_time: Optional[datetime] = None
    expire_time: Optional[datetime] = None
    create_time: Optional[datetime] = None
    class Config:
        from_attributes = True

class RiskSave(BaseModel):
    id: Optional[int] = None
    type: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    target_name: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[int] = None
    reason: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    block_type: Optional[str] = None
    block_days: Optional[int] = None
    status: str = 'pending'

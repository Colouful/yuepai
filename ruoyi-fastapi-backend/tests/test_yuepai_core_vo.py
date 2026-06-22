import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from pydantic import ValidationError

from module_yuepai.entity.vo.core_vo import DemandCreate, QuoteCreate


class DemandCreateTest(unittest.TestCase):
    def valid_payload(self) -> dict:
        now = datetime.now()
        return {
            'title': '周末城市人像拍摄',
            'description': '寻找擅长自然光人像的摄影师，拍摄完成后需要交付十张精修照片。',
            'demandType': '人像',
            'cityCode': '北京',
            'shootAt': now + timedelta(days=7),
            'durationMinutes': 180,
            'roles': ['摄影师'],
            'referenceAssets': [],
            'budgetType': 'fixed',
            'budgetMin': 500,
            'budgetMax': None,
            'applicantLimit': 20,
            'applicationDeadline': now + timedelta(days=5),
        }

    def test_valid_demand(self):
        model = DemandCreate.model_validate(self.valid_payload())
        self.assertEqual(model.budget_min, Decimal('500'))
        self.assertEqual(model.roles, ['摄影师'])

    def test_deadline_must_be_before_shooting(self):
        payload = self.valid_payload()
        payload['applicationDeadline'] = payload['shootAt'] + timedelta(hours=1)
        with self.assertRaises(ValidationError):
            DemandCreate.model_validate(payload)

    def test_range_budget_must_be_ordered(self):
        payload = self.valid_payload()
        payload.update({'budgetType': 'range', 'budgetMin': 1000, 'budgetMax': 500})
        with self.assertRaises(ValidationError):
            DemandCreate.model_validate(payload)


class QuoteCreateTest(unittest.TestCase):
    def test_fee_total_must_match_quote(self):
        with self.assertRaises(ValidationError):
            QuoteCreate.model_validate(
                {
                    'receiverUserId': 2,
                    'amount': 1000,
                    'feeBreakdown': {'shooting': 800, 'makeup': 100},
                    'serviceSnapshot': {'title': '人像写真'},
                    'expiresAt': datetime.now() + timedelta(days=1),
                }
            )


if __name__ == '__main__':
    unittest.main()

from common.router import APIRouterPro


async def health_check() -> dict:
    return {'status': 'ok'}


demand_runtime = APIRouterPro(prefix='/yuepai/health', order_num=30, tags=['91约拍Pro'])
demand_runtime.add_api_route('', health_check, methods=['GET'])

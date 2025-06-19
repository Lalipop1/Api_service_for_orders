from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.models.order import Order, OrderDishAssociation
from app.models.dish import Dish
from app.schemas.order import OrderCreate, OrderStatusUpdate

VALID_STATUSES = ["в обработке", "готовится", "доставляется", "завершен"]
STATUS_FLOW = {
    "в обработке": ["готовится", "отменен"],
    "готовится": ["доставляется"],
    "доставляется": ["завершен"],
}

async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()

async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

async def create_order(db: AsyncSession, order: OrderCreate):
    dishes = []
    for dish_id in order.dish_ids:
        dish = await db.get(Dish, dish_id)
        if not dish:
            return None
        dishes.append(dish)
    
    db_order = Order(
        customer_name=order.customer_name,
        status="в обработке"
    )
    db.add(db_order)
    await db.flush()  

    for dish in dishes:
        association = OrderDishAssociation(order_id=db_order.id, dish_id=dish.id)
        db.add(association)
    
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def delete_order(db: AsyncSession, order_id: int):
    order = await get_order(db, order_id)
    if order and order.status == "в обработке":
        await db.delete(order)
        await db.commit()
        return True
    return False

async def update_order_status(db: AsyncSession, order_id: int, status_update: OrderStatusUpdate):
    order = await get_order(db, order_id)
    if not order:
        return None
    
    new_status = status_update.status
    
    if new_status not in VALID_STATUSES:
        return None
    
    allowed_next_statuses = STATUS_FLOW.get(order.status, [])
    if new_status not in allowed_next_statuses and new_status != order.status:
        return None
    
    order.status = new_status
    await db.commit()
    await db.refresh(order)
    return order
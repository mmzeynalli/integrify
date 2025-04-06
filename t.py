from integrify.payriff import PayriffClient
from integrify.payriff.schemas.enums import Operation

# c_o = PayriffClient.create_order(
#     amount=10.0,
#     description="Test payment",
#     operation=Operation.PRE_AUTH,
#     callback_url='https://2b75-46-18-68-113.ngrok-free.app'
# )
# print(c_o)

c = PayriffClient.complete(
    order_id='9f32706c-12b6-488e-88ae-41ed756b0db8',
    amount=10.0
)

print(c)


# get_t = PayriffClient.get_order_info(
#     order_id='6df74810-4cee-43b6-a82e-ba28cfae0273'
# )

# print(get_t)
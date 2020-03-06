import braintree
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id= os.getenv('merchant_id'),
        public_key=os.getenv('public_key'),
        private_key=os.getenv('private_key')
    )
)


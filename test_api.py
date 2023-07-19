import unittest
import responses
from dataclasses import dataclass
from typing import List, Dict, Union
from api import SwagUpApiClient

@dataclass
class CreateDesignResponse:
    design_id: str
    designer_id: str
    design_name: str
    design_description: str
    categories: List[str]
    tags: List[str]
    price: float
    design_url: str

@dataclass
class UploadImageResponse:
    image_id: str
    image_url: str

@dataclass
class GetDesignDetailsResponse:
    design_id: str
    designer_id: str
    design_name: str
    design_description: str
    categories: List[str]
    tags: List[str]
    price: float
    design_url: str
    image_id: str
    image_url: str
    image_upload_timestamp: str
    image_size: str
    image_format: str

@dataclass
class ChooseLogoColorResponse:
    design_id: str
    color: Dict[str, Union[str, List[int]]]
    design_url: str

@dataclass
class SelectSizeAndQuantityResponse:
    design_id: str
    items: List[Dict[str, Union[str, int]]]
    design_url: str

@dataclass
class SetShippingDestinationResponse:
    design_id: str
    address: Dict[str, str]
    design_url: str

@dataclass
class ManagePaymentMethodsResponse:
    payment_method_id: str
    design_url: str

@dataclass
class PlaceOrderResponse:
    order_id: str
    design_url: str

@dataclass
class TrackOrderResponse:
    order_id: str
    design_url: str

@dataclass
class CancelOrderResponse:
    order_id: str
    design_url: str

class SwagUpApiClientTests(unittest.TestCase):
    def setUp(self):
        # Create an instance of SwagUpApiClient
        self.client = SwagUpApiClient(base_url="https://api.example.com", api_key="your_api_key")

    @responses.activate
    def test_create_design(self):
        expected_payload = {
            "designerId": "designer123",
            "designName": "Cool Cat",
            "designDescription": "Cat wearing sunglasses",
            "categories": ["Animals", "Humor"],
            "tags": ["cat", "cool", "sunglasses"],
            "price": 19.99
        }
        response_data = {
            "status": "success",
            "message": "Design created successfully",
            "data": {
                "designId": "123",
                "designerId": "designer123",
                "designName": "Cool Cat",
                "designDescription": "Cat wearing sunglasses",
                "categories": ["Animals", "Humor"],
                "tags": ["cat", "cool", "sunglasses"],
                "price": 19.99,
                "timestamp": "2023-07-10T15:00:00Z"
            }
        }

        responses.add(responses.POST, "https://api.example.com/designs", json=response_data, status=200)

        response = self.client.create_design(
            designer_id=expected_payload["designerId"],
            design_name=expected_payload["designName"],
            design_description=expected_payload["designDescription"],
            categories=expected_payload["categories"],
            tags=expected_payload["tags"],
            price=expected_payload["price"]
        )

        self.assertIsInstance(response, CreateDesignResponse)
        self.assertEqual(response.design_id, response_data["data"]["designId"])
        self.assertEqual(response.designer_id, response_data["data"]["designerId"])
        self.assertEqual(response.design_name, response_data["data"]["designName"])
        self.assertEqual(response.design_description, response_data["data"]["designDescription"])
        self.assertEqual(response.categories, response_data["data"]["categories"])
        self.assertEqual(response.tags, response_data["data"]["tags"])
        self.assertEqual(response.price, response_data["data"]["price"])
        self.assertEqual(response.design_url, response_data["data"]["timestamp"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/designs")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertDictEqual(responses.calls[0].request.json(), expected_payload)

    @responses.activate
    def test_upload_image(self):
        expected_image_file = "/path/to/image.png"
        response_data = {
            "status": "success",
            "message": "Image uploaded successfully",
            "data": {
                "imageId": "456",
                "imageUrl": "https://your-api.com/images/456",
                "uploadTimestamp": "2023-07-10T15:05:00Z",
                "imageSize": "1.5MB",
                "imageFormat": "png"
            }
        }

        responses.add(responses.POST, "https://api.example.com/images", json=response_data, status=200)

        response = self.client.upload_image(image=expected_image_file)

        self.assertIsInstance(response, UploadImageResponse)
        self.assertEqual(response.image_id, response_data["data"]["imageId"])
        self.assertEqual(response.image_url, response_data["data"]["imageUrl"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/images")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertIn("multipart/form-data", responses.calls[0].request.headers["Content-Type"])

    @responses.activate
    def test_get_design_details(self):
        design_id = "123"
        response_data = {
            "status": "success",
            "message": "Design details fetched successfully",
            "data": {
                "designId": "123",
                "designerId": "designer123",
                "designName": "Cool Cat",
                "designDescription": "Cat wearing sunglasses",
                "categories": ["Animals", "Humor"],
                "tags": ["cat", "cool", "sunglasses"],
                "price": 19.99,
                "creationTimestamp": "2023-07-10T15:00:00Z",
                "imageId": "456",
                "imageUrl": "https://your-api.com/images/456",
                "imageUploadTimestamp": "2023-07-10T15:05:00Z",
                "imageSize": "1.5MB",
                "imageFormat": "png"
            }
        }

        responses.add(responses.GET, f"https://api.example.com/designs/{design_id}", json=response_data, status=200)

        response = self.client.get_design_details(design_id)

        self.assertIsInstance(response, GetDesignDetailsResponse)
        self.assertEqual(response.design_id, response_data["data"]["designId"])
        self.assertEqual(response.designer_id, response_data["data"]["designerId"])
        self.assertEqual(response.design_name, response_data["data"]["designName"])
        self.assertEqual(response.design_description, response_data["data"]["designDescription"])
        self.assertEqual(response.categories, response_data["data"]["categories"])
        self.assertEqual(response.tags, response_data["data"]["tags"])
        self.assertEqual(response.price, response_data["data"]["price"])
        self.assertEqual(response.design_url, response_data["data"]["creationTimestamp"])
        self.assertEqual(response.image_id, response_data["data"]["imageId"])
        self.assertEqual(response.image_url, response_data["data"]["imageUrl"])
        self.assertEqual(response.image_upload_timestamp, response_data["data"]["imageUploadTimestamp"])
        self.assertEqual(response.image_size, response_data["data"]["imageSize"])
        self.assertEqual(response.image_format, response_data["data"]["imageFormat"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, f"https://api.example.com/designs/{design_id}")
        self.assertEqual(responses.calls[0].request.method, "GET")

    @responses.activate
    def test_choose_logo_color(self):
        design_id = "123"
        expected_payload = {
            "color": {
                "name": "Red",
                "hex": "#FF0000",
                "rgb": [255, 0, 0]
            },
            "designId": design_id
        }
        response_data = {
            "status": "success",
            "message": "Logo color set successfully",
            "data": {
                "designId": design_id,
                "logoColor": {
                    "name": "Red",
                    "hex": "#FF0000",
                    "rgb": [255, 0, 0]
                }
            }
        }

        responses.add(responses.POST, "https://api.example.com/logo-color", json=response_data, status=200)

        response = self.client.choose_logo_color(design_id=design_id, color=expected_payload["color"])

        self.assertIsInstance(response, ChooseLogoColorResponse)
        self.assertEqual(response.design_id, response_data["data"]["designId"])
        self.assertEqual(response.color, response_data["data"]["logoColor"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/logo-color")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertDictEqual(responses.calls[0].request.json(), expected_payload)

    @responses.activate
    def test_select_size_and_quantity(self):
        design_id = "123"
        expected_payload = {
            "designId": design_id,
            "items": [
                {"size": "S", "quantity": 50},
                {"size": "M", "quantity": 100},
                {"size": "L", "quantity": 50}
            ]
        }
        response_data = {
            "status": "success",
            "message": "Sizes and quantities set successfully",
            "data": {
                "designId": design_id,
                "items": [
                    {"size": "S", "quantity": 50},
                    {"size": "M", "quantity": 100},
                    {"size": "L", "quantity": 50}
                ]
            }
        }

        responses.add(responses.POST, "https://api.example.com/orders/sizes-quantity", json=response_data, status=200)

        response = self.client.select_size_and_quantity(design_id=design_id, items=expected_payload["items"])

        self.assertIsInstance(response, SelectSizeAndQuantityResponse)
        self.assertEqual(response.design_id, response_data["data"]["designId"])
        self.assertEqual(response.items, response_data["data"]["items"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/orders/sizes-quantity")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertDictEqual(responses.calls[0].request.json(), expected_payload)

    @responses.activate
    def test_set_shipping_destination(self):
        design_id = "123"
        expected_payload = {
            "designId": design_id,
            "address": {
                "recipientName": "John Doe",
                "street": "123 Swag Street",
                "city": "Swag City",
                "state": "Swag State",
                "country": "Swag Country",
                "zip": "12345"
            }
        }
        response_data = {
            "status": "success",
            "message": "Shipping address set successfully",
            "data": {
                "designId": design_id,
                "address": {
                    "recipientName": "John Doe",
                    "street": "123 Swag Street",
                    "city": "Swag City",
                    "state": "Swag State",
                    "country": "Swag Country",
                    "zip": "12345"
                }
            }
        }

        responses.add(responses.POST, "https://api.example.com/orders/shipping", json=response_data, status=200)

        response = self.client.set_shipping_destination(design_id=design_id, address=expected_payload["address"])

        self.assertIsInstance(response, SetShippingDestinationResponse)
        self.assertEqual(response.design_id, response_data["data"]["designId"])
        self.assertEqual(response.address, response_data["data"]["address"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/orders/shipping")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertDictEqual(responses.calls[0].request.json(), expected_payload)

    @responses.activate
    def test_manage_payment_methods(self):
        expected_payload = {
            "paymentMethod": {
                "type": "credit card",
                "cardNumber": "1234567812345678",
                "expiryDate": "07/25",
                "cvv": "123"
            }
        }
        response_data = {
            "status": "success",
            "message": "Payment method added successfully",
            "data": {
                "paymentMethodId": "payment123",
                "type": "credit card",
                "expiryDate": "07/25"
            }
        }

        responses.add(responses.POST, "https://api.example.com/payment-methods", json=response_data, status=200)

        response = self.client.manage_payment_methods(payment_method=expected_payload["paymentMethod"])

        self.assertIsInstance(response, ManagePaymentMethodsResponse)
        self.assertEqual(response.payment_method_id, response_data["data"]["paymentMethodId"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/payment-methods")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertDictEqual(responses.calls[0].request.json(), expected_payload)

    @responses.activate
    def test_place_order(self):
        design_id = "123"
        payment_method_id = "payment123"
        expected_payload = {
            "designId": design_id,
            "paymentMethodId": payment_method_id
        }
        response_data = {
            "status": "success",
            "message": "Order placed successfully",
            "data": {
                "orderId": "order123",
                "designId": design_id,
                "paymentMethodId": payment_method_id,
                "status": "Processing",
                "timestamp": "2023-07-10T16:00:00Z"
            }
        }

        responses.add(responses.POST, "https://api.example.com/orders", json=response_data, status=200)

        response = self.client.place_order(design_id=design_id, payment_method_id=payment_method_id)

        self.assertIsInstance(response, PlaceOrderResponse)
        self.assertEqual(response.order_id, response_data["data"]["orderId"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.example.com/orders")
        self.assertEqual(responses.calls[0].request.method, "POST")
        self.assertDictEqual(responses.calls[0].request.json(), expected_payload)

    @responses.activate
    def test_track_order(self):
        order_id = "order123"
        response_data = {
            "status": "success",
            "message": "Order fetched successfully",
            "data": {
                "orderId": order_id,
                "designId": "123",
                "status": "Shipped",
                "timestamp": "2023-07-10T16:00:00Z",
                "shippingAddress": {
                    "recipientName": "John Doe",
                    "street": "123 Swag Street",
                    "city": "Swag City",
                    "state": "Swag State",
                    "country": "Swag Country",
                    "zip": "12345"
                },
                "estimatedDelivery": "2023-07-17T16:00:00Z"
            }
        }

        responses.add(responses.GET, f"https://api.example.com/orders/{order_id}", json=response_data, status=200)

        response = self.client.track_order(order_id)

        self.assertIsInstance(response, TrackOrderResponse)
        self.assertEqual(response.order_id, response_data["data"]["orderId"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, f"https://api.example.com/orders/{order_id}")
        self.assertEqual(responses.calls[0].request.method, "GET")

    @responses.activate
    def test_cancel_order(self):
        order_id = "order123"
        response_data = {
            "status": "success",
            "message": "Order cancelled successfully",
            "data": {
                "orderId": order_id,
                "status": "Cancelled"
            }
        }

        responses.add(responses.DELETE, f"https://api.example.com/orders/{order_id}", json=response_data, status=200)

        response = self.client.cancel_order(order_id)

        self.assertIsInstance(response, CancelOrderResponse)
        self.assertEqual(response.order_id, response_data["data"]["orderId"])

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, f"https://api.example.com/orders/{order_id}")
        self.assertEqual(responses.calls[0].request.method, "DELETE")

if __name__ == "__main__":
    unittest.main()

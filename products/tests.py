from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']),
                         list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']),
                         list(self.products.filter(category_id=category.id)[:3])
                         )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

    # @staticmethod
    # def get_quantity_products_by_page(response) -> int | None:
    #     paginator = response.context_data.get('paginator')
    #     return paginator.per_page if pginator else None
    #
    # def get_list_products(self, response, filter_args: dict = None) -> list:
    #     if filter_args:
    #         list_products = Product.objects.filter(**filter_args)
    #     else:
    #         list_products = Product.objects.all()
    #
    #     quantity_products_by_page = get_quantity_products_by_page(response)
    #     if quantity_products_by_page:
    #         list_products = list_products[:quantity_products_by_page]
    #
    #     return list(list_products)

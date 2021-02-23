# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import warnings
from datetime import datetime

from trytond.pool import Pool
from trytond.rpc import RPC
from trytond.transaction import Transaction
from trytond.pyson import Eval, Bool
from trytond.model import ModelView, fields, ModelSQL, Unique
from dateutil.relativedelta import relativedelta
from trytond.modules.company.company import TIMEZONES

from trytond.i18n import gettext
from trytond.exceptions import UserError

STATES = {
    'readonly': ~Eval('active', True),
}
DEPENDS = ['active']

PRODUCT_STATES = {
    'invisible': ~(Eval('source') != 'manual'),
    'required': Eval('source') != 'manual',
}

INVISIBLE_IF_MANUAL = {
    'invisible': Eval('source') == 'manual',
}


class SaleChannel(ModelSQL, ModelView):
    __name__ = 'sale.channel'

    shipping_carriers = fields.One2Many(
        'sale.channel.carrier', 'channel', 'Shipping Carriers'
    )

    @classmethod
    def __setup__(cls):
        super(SaleChannel, cls).__setup__()
        cls._buttons.update({
            'import_shipping_carriers': {},
        })

    @classmethod
    def view_attributes(cls):
        invisible = Eval('source').in_(['manual', 'pos'])
        return super(SaleChannel, cls).view_attributes() + [
            ('//page[@id="shipping_carriers"]', 'states', {
                    'invisible': invisible,
                    })
            ]

    @classmethod
    @ModelView.button
    def import_shipping_carriers(cls, channels):
        """
        Create shipping carriers by importing data from external channel.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to reuse this method or call super.

        :param instances: Active record list of magento instances
        """
        raise NotImplementedError("This feature has not been implemented.")

    def get_shipping_carrier(self, code, name, silent=False):
        """
        Search for an existing carrier by matching code and channel.
        If found, return its active record else raise_user_error.
        """
        pool = Pool()
        SaleCarrierChannel = pool.get('sale.channel.carrier')

        try:
            carrier, = SaleCarrierChannel.search([
                ('code', 'ilike', code),
                ('channel', '=', self.id),
            ], limit=1)
            # limit=1 is done to handle concurrency issue
        except ValueError:
            if silent:
                return None
            raise UserError(gettext('sale_channel.no_carriers_found',
                    code,))
        else:
            return carrier

    def get_shipping_carrier_service(self, code, silent=False):
        """
        Search for an existing carrier service by matching code and channel.
        If found, return its active record else raise_user_error.
        """
        pool = Pool()
        SaleCarrierChannel = pool.get('sale.channel.carrier')

        try:
            carrier, = SaleCarrierChannel.search([
                ('code', 'ilike', code),
                ('channel', '=', self.id),
            ], limit=1)
        except ValueError:
            if silent:
                return None
            raise UserError(gettext('sale_channel.no_carriers_found',
                    code))
        else:
            return carrier.carrier_service

    def get_order_states_to_import(self):
        """
        Return list of `sale.channel.order_state` to import orders
        """
        pool = Pool()
        OrderState = pool.get('sale.channel.order_state')

        order_states_to_import = ['process_automatically', 'process_manually']
        if Transaction().context.get('include_past_orders', False):
            order_states_to_import.append('import_as_past')

        order_states = OrderState.search([
            ('action', 'in', order_states_to_import),
            ('channel', '=', self.id),
        ])
        if not order_states:
            raise UserError(gettext("sale_channel.no_order_states_to_import"))
        return order_states

    def export_product_prices(self):
        """
        Export product prices to channel

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to reuse this method or call super.

        :return: List of active records of products for which prices are
        exported
        """
        raise NotImplementedError(
            "This feature has not been implemented for %s channel yet."
            % self.source)

    def export_order_status(self):
        """
        Export order status to external channel

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to reuse this method or call super.

        :return: List of active records of orders exported
        """
        raise NotImplementedError(
            "This feature has not been implemented for %s channel yet."
            % self.source)

    @classmethod
    def import_orders_using_cron(cls):  # pragma: nocover
        """
        Cron method to import orders from channels using cron

        Downstream module need not to implement this method.
        It will automatically call import_orders of the channel
        Silently pass if import_orders is not implemented
        """
        for channel in cls.search([]):
            with Transaction().set_context(company=channel.company.id):
                try:
                    channel.import_orders()
                except NotImplementedError:
                    # Silently pass if method is not implemented
                    pass

    @classmethod
    def export_product_prices_using_cron(cls):  # pragma: nocover
        """
        Cron method to export product prices to external channel using cron

        Downstream module need not to implement this method.
        It will automatically call export_product_prices method of the channel.
        Silently pass if export_product_prices is not implemented
        """
        for channel in cls.search([]):
            with Transaction().set_context(company=channel.company.id):
                try:
                    channel.export_product_prices()
                except NotImplementedError:
                    # Silently pass if method is not implemented
                    pass

    @classmethod
    def export_order_status_using_cron(cls):
        """
        Export sales orders status to external channel using cron
        """
        for channel in cls.search([]):
            try:
                channel.export_order_status()
            except NotImplementedError:
                pass

    def get_listings_to_export_inventory(self):
        warnings.warn(
            "Method 'sale.channel.get_listings_to_export_inventory' is "
            "deprecated, use 'get_listings_updated_after' instead",
            DeprecationWarning, stacklevel=2
        )
        return self.get_listings_updated_after(self.last_inventory_export_time)

    def get_listings_updated_after(self, updated_after=None):
        """
        This method returns listing, which needs inventory update

        Downstream module can override change its implementation

        :return: List of AR of `product.product.channel_listing`
        """
        ChannelListing = pool.get('product.product.channel_listing')
        cursor = Transaction().connection.cursor()

        if not updated_after:
            # Return all active listings
            return ChannelListing.search([
                ('channel', '=', self),
                ('state', '=', 'active')
            ])
        else:
            # Query to find listings
            #   in which product inventory is recently updated or
            #   listing it self got updated recently
            cursor.execute("""
                SELECT listing.id
                FROM product_product_channel_listing AS listing
                INNER JOIN stock_move ON stock_move.product = listing.product
                WHERE listing.channel = %s AND listing.state = 'active' AND
                (
                    COALESCE(stock_move.write_date, stock_move.create_date) > %s
                    OR
                    COALESCE(listing.write_date, listing.create_date) > %s
                )
                GROUP BY listing.id
            """, (
                self.id, updated_after, updated_after
            ))
            listing_ids = [r[0] for r in cursor.fetchall()]
            return ChannelListing.browse(listing_ids)

    def export_inventory(self):
        """
        Export inventory to external channel
        """
        pool = Pool()
        Listing = pool.get('product.product.channel_listing')
        Channel = pool.get('sale.channel')

        last_inventory_export_time = datetime.utcnow()
        channel_id = self.id

        listings = self.get_listings_updated_after(
            self.last_inventory_export_time)
        # TODO: check if inventory export is allowed for this channel
        Listing.export_bulk_inventory(listings)

        # XXX: Exporting inventory to external channel is an expensive.
        # To avoid lock on sale_channel table save record after
        # exporting all inventory
        with Transaction().new_transaction() as txn:
            channel = Channel(channel_id)
            channel.last_inventory_export_time = last_inventory_export_time
            channel.save()
            txn.commit()

    @classmethod
    def export_inventory_from_cron(cls):  # pragma: nocover
        """
        Cron method to export inventory to external channel
        """
        for channel in cls.search([]):
            with Transaction().set_context(company=channel.company.id):
                try:
                    channel.export_inventory()
                except NotImplementedError:
                    # Silently pass if method is not implemented
                    pass

    def import_orders(self):
        """
        Import orders from external channel.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement importing or call
        super to delegate.

        :return: List of active records of sale orders that are imported
        """
        raise NotImplementedError(
            "Import orders is not implemented for %s channels" % self.source)

    def import_order(self, order_info):
        """
        Import specific order from external channel based on order_info.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement importing or call
        super to delegate.

        :param order_info: The type of order_info depends on the channel. It
                           could be an integer ID, a dictionary or anything.

        :return: imported sale order active record
        """
        raise NotImplementedError(
            "Import order is not implemented for %s channels" % self.source)

    def import_products(self):
        """
        Import Products from external channel.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement importing or call
        super to delegate.

        :return: List of active records of products that are imported
        """
        raise NotImplementedError(
            "Method import_products is not implemented for %s channel yet"
            % self.source)  # pragma: nocover

    @classmethod
    def import_products_using_cron(cls):  # pragma: nocover
        """
        Method to import products from channels using cron

        Downstream module need not to implement this method.
        It will automatically call import_products of the channel
        Silently pass if import_products is not implemented
        """
        for channel in cls.search([]):
            with Transaction().set_context(company=channel.company.id):
                try:
                    channel.import_products()
                except NotImplementedError:
                    # Silently pass if method is not implemented
                    pass

    def import_product(self, identifier, product_data=None):
        """
        Import specific product from external channel based on product
        identifier.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement importing or call
        super to delegate.

        :param identifier: product code or sku

        :return: imported product active record
        """
        raise NotImplementedError(
            "Method import_product is not implemented for %s channel yet"
            % self.source)  # pragma: nocover

    def get_product(self, identifier, product_data=None):
        """
        Given a SKU find the product or if it aint there create it and then
        return the active record of the product. This cannot be done async
        under any circumstances, because a product created on another
        transaction will not be visible to the current transaction unless the
        transaction is started over.

        :param identifier: product identifier
        """
        return self.import_product(identifier, product_data)

    def import_product_images(self):
        """
        Helper method for importing product images from external channel
        after products are imported.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement importing or call
        super to delegate.
        """
        pool = Pool()
        ProductListing = pool.get('product.product.channel_listing')

        product_listings = ProductListing.search([
            ('channel', '=', self.id),
            ('state', '=', 'active'),
        ])
        if not product_listings:
            raise UserError(gettext('no_active_listing'))

        for listing in product_listings:
            listing.import_product_image()

    @classmethod
    @ModelView.button_action('sale_channel.wizard_import_data')
    def import_data_button(cls, channels):
        pass  # pragma: nocover

    @classmethod
    @ModelView.button_action('sale_channel.wizard_export_data')
    def export_data_button(cls, channels):
        pass  # pragma: nocover

    @classmethod
    @ModelView.button_action('sale_channel.wizard_import_order_states')
    def import_order_states_button(cls, channels):
        """
        Import order states for current channel

        :param channels: List of active records of channels
        """
        pass

    def import_order_states(self):
        """
        Imports order states for current channel

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement importing or call
        super to delegate.
        """
        raise NotImplementedError(
            "This feature has not been implemented for %s channel yet"
            % self.source)

    def get_default_tryton_action(self, code, name=None):
        """
        Return default tryton_actions for this channel
        """
        return {
            'action': 'do_not_import',
            'invoice_method': 'manual',
            'shipment_method': 'manual',
        }

    def get_tryton_action(self, code):
        """
        Get the tryton action corresponding to the channel state
        as per the predefined logic.

        Downstream modules need to inherit method and map states as per
        convenience.

        :param code: Code of channel state
        :returns: A dictionary of tryton action and shipment and invoice methods
        """
        pool = Pool()
        ChannelOrderState = pool.get('sale.channel.order_state')

        try:
            order_state, = ChannelOrderState.search([
                ('channel', '=', self.id),
                ('code', '=', code),
            ])
        except ValueError:
            return {
                'action': 'do_not_import',
                'invoice_method': 'manual',
                'shipment_method': 'manual',
            }
        else:
            return {
                'action': order_state.action,
                'invoice_method': order_state.invoice_method,
                'shipment_method': order_state.shipment_method,
            }

    def create_order_state(self, code, name):
        """
        This method creates order state for channel with given state code and
        state name. If state already exist, return same.

        :param code: State code used by external channel
        :param name: State name used by external channel
        :return: Active record of order state created or found
        """
        pool = Pool()
        OrderState = pool.get('sale.channel.order_state')

        order_states = OrderState.search([
            ('code', '=', code),
            ('channel', '=', self.id)
        ])

        if order_states:
            return order_states[0]

        values = self.get_default_tryton_action(code, name)
        values.update({
            'name': name,
            'code': code,
            'channel': self.id,
        })

        return OrderState.create([values])[0]

    def get_availability_context(self):
        """
        Return the context in which the stock availability of any product must
        be computed
        """
        return {
            'locations': [self.warehouse.id],
        }

    def get_availability(self, product):
        """
        Return availability of the product within the context of this channel

        Availability consists of three factors:

            type: finite, bucket, infinite
            quantity: (optional) quantity available
            value: in_stock, limited, out_of_stock

        If this looks like the value in the stripe relay API, do not be
        confused, they are the same :)
        """
        pool = Pool()
        Listing = pool.get('product.product.channel_listing')
        Product = pool.get('product.product')

        listings = Listing.search([
            ('channel', '=', self.id),
            ('product', '=', product),
        ])
        if listings:
            # If there are listings, return the values from listing since
            # they override channel defaults for a product and channel
            return listings[0].get_availability()

        with Transaction().set_context(**self.get_availability_context()):
            rv = {'type': 'bucket'}
            quantity = Product.get_quantity([product], 'quantity')[product.id]
            if quantity > 0:
                rv['value'] = 'in_stock'
            else:
                rv['value'] = 'out_of_stock'

        return rv

    @classmethod
    def update_order_status_using_cron(cls):  # pragma: nocover
        """
        Cron method to update orders from channels using cron

        Downstream module need not to implement this method.
        It will automatically call update_order_status of the channel
        Silently pass if update_order_status is not implemented
        """
        for channel in cls.search([]):
            with Transaction().set_context(company=channel.company.id):
                try:
                    channel.update_order_status()
                except NotImplementedError:
                    # Silently pass if method is not implemented
                    pass

    def update_order_status(self):
        """This method is responsible for updating order status from external
        channel.
        """
        if self.source == 'manual':
            return
        raise NotImplementedError(
            "This feature has not been implemented for %s channel yet."
            % self.source)

    def get_tax(self, name, rate, silent=False):
        """
        Search for an existing Tax record by matching name and rate.
        If found return its active record else raise user error.
        """
        pool = Pool()
        TaxMapping = pool.get('sale.channel.tax')
        domain = [
            ('rate', '=', rate),
            ('channel', '=', self)
        ]
        if name:
            # Search with name when it is provided
            # Name can be explicitly passed as None, when external
            # channels like magento does not provide it.
            domain.append(('name', '=', name))

        try:
            mapped_tax, = TaxMapping.search(domain)
        except ValueError:
            if silent:
                return None
            raise UserError(gettext('no_tax_found',
                    name, rate,))
        else:
            return mapped_tax.tax


class ReadUser(ModelSQL):
    """
    Read Users for Sale Channel
    """
    __name__ = 'sale.channel-read-res.user'

    channel = fields.Many2One(
        'sale.channel', 'Channel', ondelete='CASCADE', select=True,
        required=True
    )
    user = fields.Many2One(
        'res.user', 'User', ondelete='RESTRICT', required=True
    )


class WriteUser(ModelSQL):
    """
    Write Users for Sale Channel
    """
    __name__ = 'sale.channel-write-res.user'

    channel = fields.Many2One(
        'sale.channel', 'Channel', ondelete='CASCADE', select=True,
        required=True
    )
    user = fields.Many2One(
        'res.user', 'User', ondelete='RESTRICT', required=True
    )


class ChannelException(ModelSQL, ModelView):
    """
    Channel Exception model
    """
    __name__ = 'channel.exception'

    origin = fields.Reference(
        "Origin", selection='models_get', select=True, readonly=True
    )
    log = fields.Text('Exception Log', readonly=True)
    channel = fields.Many2One(
        "sale.channel", "Channel", required=True, readonly=True
    )
    is_resolved = fields.Boolean("Is Resolved ?", select=True)

    @classmethod
    def __setup__(cls):
        """
        Setup the class before adding to pool
        """
        super(ChannelException, cls).__setup__()

        cls._buttons.update({
            'resolve_exception_button': {
                'readonly': Bool(Eval('is_resolved')),
            },
        })

    @classmethod
    @ModelView.button
    def resolve_exception_button(cls, exceptions):
        """
        Method called from a button to resolve exceptions

        :param channels: List of active records of exceptions
        """
        for exception in exceptions:
            if exception.is_resolved:
                continue
            exception.is_resolved = True
            exception.save()

    @staticmethod
    def default_is_resolved():
        return False

    @classmethod
    def models_get(cls):
        '''
        Return valid models allowed for origin
        '''
        return [
            ('sale.sale', 'Sale'),
            ('sale.line', 'Sale Line'),
        ]


class ChannelOrderState(ModelSQL, ModelView):
    """
    Sale Channel - Tryton Order State map

    This model stores a map of order states between tryton and sale channel.
    This allows the user to configure the states mapping according to his/her
    convenience. This map is used to process orders in tryton when they are
    imported. This is also used to map the order status back to channel when
    sales are exported. This also allows the user to determine in which state
    order need to be imported.
    """
    __name__ = 'sale.channel.order_state'

    name = fields.Char('Name', required=True, readonly=True)
    code = fields.Char('Code', required=True, readonly=True)
    action = fields.Selection([
        ('do_not_import', 'Do Not Import'),
        ('process_automatically', 'Process Automatically'),
        ('process_manually', 'Process Manually'),
        ('import_as_past', 'Import As Past Orders'),
    ], 'Action', required=True)
    invoice_method = fields.Selection([
        ('manual', 'Manual'),
        ('order', 'On Order Processed'),
        ('shipment', 'On Shipment Sent'),
    ], 'Invoice Method', required=True)
    shipment_method = fields.Selection([
        ('manual', 'Manual'),
        ('order', 'On Order Processed'),
        ('invoice', 'On Invoice Paid'),
    ], 'Shipment Method', required=True)
    channel = fields.Many2One(
        'sale.channel', 'Sale Channel', required=True,
        ondelete="CASCADE", readonly=True
    )

    @staticmethod
    def default_channel():
        "Return default channel from context"
        return Transaction().context.get('current_channel')


class TaxMapping(ModelSQL, ModelView):
    'Sale Tax'
    __name__ = 'sale.channel.tax'

    name = fields.Char("Name", required=True)
    rate = fields.Numeric('Rate', digits=(14, 10), required=True)
    tax = fields.Many2One("account.tax", "Tax", required=True)
    channel = fields.Many2One("sale.channel", "Channel", required=True)

    @classmethod
    def __setup__(cls):
        super(TaxMapping, cls).__setup__()

        table = cls.__table__()
        cls._sql_constraints += [
            ('unique_tax_percent',
             Unique(table, table.channel, table.name, table.rate),
             'unique_tax_rate_per_channel')
        ]

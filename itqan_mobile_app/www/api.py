import json
import base64
import os
from collections.abc import Iterable
from six import string_types
import frappe
from frappe.utils import flt
from frappe import _
from frappe.utils import get_files_path
from frappe.utils.file_manager import save_file

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:        
            yield item

@frappe.whitelist(allow_guest=True)
def get_user(user):
    doc = frappe.get_doc("User", user)
    return {"user": doc, "type": "user"}

@frappe.whitelist()
def get_items_list(filters=None):
    return frappe.db.get_list("Item", filters=filters, fields="name")

@frappe.whitelist()
def create_payment(args):
    if isinstance(args, string_types):
        args = json.loads(args)

    if not frappe.has_permission("Payment Entry", ptype= "write", user=args.get("owner")):
        return {"error": "Not Permitted", "status": 0}

    doc = frappe.new_doc("Payment Entry")

    tables = doc.meta.get_table_fields()
    tables_names = {}
    if tables:
        for df in tables:
            tables_names[df.fieldname] = df.options

    for field in args:
        if field in tables_names:
            for d in args.get(field):
                new_doc = frappe.new_doc(tables_names[field], as_dict=True)
                for attr in d:
                    if hasattr(new_doc, attr):
                        setattr(new_doc, attr, d[attr])

                doc.append(field, new_doc)

        elif hasattr(doc, field):
            setattr(doc, field, args.get(field))

    if not doc.received_amount:
        doc.received_amount = doc.paid_amount


    try:
        doc.insert()
        frappe.db.commit()
    except Exception as e:
        return {"error": e, "status": 0}

    return {"error": 0, "status": 1}

@frappe.whitelist()
def update_payment(args):
    if isinstance(args, string_types):
        args = json.loads(args)

    if not frappe.has_permission("Payment Entry", ptype= "write", user=args.get("owner")):
        return {"error": "Not Permitted", "status": 0}

    if not args.get("payment_entry"):
        return {"error": "No Payment Entry is Specified", "status": 0}

    if not frappe.db.exists("Payment Entry", args.get("payment_entry")):
        return {"error": "No Payment Entry with the Name {}".format(args.get("payment_entry")), "status": 0}

    payment_entry = frappe.get_doc("Payment Entry", args.get("payment_entry"))

    for field in args:
        if field == "payment_entry": continue

        elif hasattr(payment_entry, field):
            setattr(payment_entry, field, args.get(field))

    try:
        payment_entry.save()
        frappe.db.commit()
    except Exception as e:
        return {"error": e, "status": 0}

    return {"error": 0, "status": 1}

@frappe.whitelist()
def get_payment_entries_list(filters=None):
    return frappe.db.get_list("Payment Entry", filters=filters, fields="name")

@frappe.whitelist()
def get_payment_entry(payment_entry):
    return frappe.get_all("Payment Entry", filters={"name": payment_entry}, fields=["*"])

@frappe.whitelist()
def create_sales_invoice(args):
    if isinstance(args, string_types):
        args = json.loads(args)

    if not frappe.has_permission("Sales Invoice", ptype= "write", user=args.get("owner")):
        return {"error": "Not Permitted", "status": 0}

    doc = frappe.new_doc("Sales Invoice")

    tables = doc.meta.get_table_fields()
    tables_names = {}
    if tables:
        for df in tables:
            tables_names[df.fieldname] = df.options

    for field in args:
        if field in tables_names:
            for d in args.get(field):
                new_doc = frappe.new_doc(tables_names[field], as_dict=True)
                for attr in d:
                    if hasattr(new_doc, attr):
                        setattr(new_doc, attr, d[attr])

                doc.append(field, new_doc)

        elif hasattr(doc, field):
            setattr(doc, field, args.get(field))

    try:
        doc.insert()
        frappe.db.commit()
    except Exception as e:
        return {"error": e, "status": 0}

    return {"error": 0, "status": 1}

@frappe.whitelist()
def update_sales_invoice(args):
    if isinstance(args, string_types):
        args = json.loads(args)

    if not frappe.has_permission("Sales Invoice", ptype= "write", user=args.get("owner")):
        return {"error": "Not Permitted", "status": 0}

    if not args.get("sales_invoice"):
        return {"error": "No Sales Invoice is Specified", "status": 0}

    if not frappe.db.exists("Sales Invoice", args.get("sales_invoice")):
        return {"error": "No Sales Invoice with the Name {}".format(args.get("sales_invoice")), "status": 0}

    sales_invoice = frappe.get_doc("Sales Invoice", args.get("sales_invoice"))

    for field in args:
        if field == "sales_invoice": continue

        elif hasattr(sales_invoice, field):
            setattr(sales_invoice, field, args.get(field))

    try:
        sales_invoice.save()
        frappe.db.commit()
    except Exception as e:
        return {"error": e, "status": 0}

    return {"error": 0, "status": 1}

@frappe.whitelist()
def get_default_company():
    return {
        "company": frappe.db.get_single_value("Global Defaults", "default_company")
    }

@frappe.whitelist()
def get_sales_invoices_list(filters=None):
    return frappe.db.get_list("Sales Invoice", filters=filters, fields="name")

@frappe.whitelist()
def get_sales_invoice(sales_invoice):
    return frappe.get_all("Sales Invoice", filters={"name": sales_invoice}, fields=["*"])

@frappe.whitelist()
def create_purchase_invoice(args):
    if isinstance(args, string_types):
        args = json.loads(args)

    if not frappe.has_permission("Purchase Invoice", ptype= "write", user=args.get("owner")):
        return {"error": "Not Permitted", "status": 0}

    doc = frappe.new_doc("Purchase Invoice")

    tables = doc.meta.get_table_fields()
    tables_names = {}
    if tables:
        for df in tables:
            tables_names[df.fieldname] = df.options

    for field in args:
        if field in tables_names:
            for d in args.get(field):
                new_doc = frappe.new_doc(tables_names[field], as_dict=True)
                for attr in d:
                    if hasattr(new_doc, attr):
                        setattr(new_doc, attr, d[attr])

                doc.append(field, new_doc)

        elif hasattr(doc, field):
            setattr(doc, field, args.get(field))

    try:
        doc.insert()
        frappe.db.commit()
    except Exception as e:
        return {"error": e, "status": 0}

    return {"error": 0, "status": 1}

@frappe.whitelist()
def update_purchase_invoice(args):
    if isinstance(args, string_types):
        args = json.loads(args)

    if not frappe.has_permission("Purchase Invoice", ptype= "write", user=args.get("owner")):
        return {"error": "Not Permitted", "status": 0}

    if not args.get("purchase_invoice"):
        return {"error": "No Purchase Invoice is Specified", "status": 0}

    if not frappe.db.exists("Purchase Invoice", args.get("purchase_invoice")):
        return {"error": "No Purchase Invoice with the Name {}".format(args.get("purchase_invoice")), "status": 0}

    purchase_invoice = frappe.get_doc("Purchase Invoice", args.get("purchase_invoice"))

    for field in args:
        if field == "purchase_invoice": continue

        elif hasattr(purchase_invoice, field):
            setattr(purchase_invoice, field, args.get(field))

    try:
        purchase_invoice.save()
        frappe.db.commit()
    except Exception as e:
        return {"error": e, "status": 0}

    return {"error": 0, "status": 1}

@frappe.whitelist()
def get_purchase_invoices_list(filters=None):
    return frappe.db.get_list("Purchase Invoice", filters=filters, fields="name")

@frappe.whitelist()
def get_purchase_invoice(purchase_invoice):
    return frappe.get_all("Purchase Invoice", filters={"name": purchase_invoice}, fields=["*"])

@frappe.whitelist()
def get_exchange_rate(from_currency, to_currency, transaction_date = None):
    from erpnext.setup.utils import get_exchange_rate

    return get_exchange_rate(from_currency, to_currency, transaction_date)

@frappe.whitelist()
def get_payment_party_details(party_type, party, date, company=None, cost_center=None):
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_party_details

    return get_party_details(company, party_type, party, date, cost_center)

@frappe.whitelist()
def get_paid_to_accounts_query(payment_type, party_type, company=None):
    if not company:
        from erpnext import get_default_company

        company = get_default_company()

    if payment_type in ["Receive", "Internal Transfer"]:
        account_types = ["Bank", "Cash"]

    else:
        if party_type == "Customer":
            account_types =  ["Receivable"]
        else: account_types = ["Payable"]

    return frappe.db.get_all("Account", {
        "company": company,
        "is_group": 0,
        "account_type": ("in", account_types)
    }, "name", as_list = 1)  


@frappe.whitelist()
def get_paid_from_accounts_query(payment_type, party_type, company=None):
    if not company:
        from erpnext import get_default_company

        company = get_default_company()

    if payment_type in ["Pay", "Internal Transfer"]:
        account_types = ["Bank", "Cash"]

    else:
        if party_type == "Customer":
            account_types =  ["Receivable"]
        else: account_types = ["Payable"]

    return frappe.db.get_all("Account", {
        "company": company,
        "is_group": 0,
        "account_type": ("in", account_types)
    }, "name", as_list = 1)  

@frappe.whitelist()
def get_outstanding_documents(args):
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_outstanding_reference_documents

    return get_outstanding_reference_documents(args)

@frappe.whitelist()
def get_conversion_factor(item_code, uom):
    from erpnext.stock.get_item_details import get_conversion_factor

    return get_conversion_factor(item_code, uom)

@frappe.whitelist()
def get_item_details(args):
    from erpnext.stock.get_item_details import get_item_details

    return get_item_details(args)

@frappe.whitelist()
def get_party_details(party_type, party, posting_date=None, company=None, account=None, price_list=None, pos_profile=None, doctype=None):
    from erpnext.accounts.party import get_party_details

    return get_party_details(party_type=party_type, party=party, posting_date=posting_date, company=company, account=account, price_list=price_list, pos_profile=pos_profile, doctype=doctype)

@frappe.whitelist()
def get_party_account(party_type, party, company):
    from erpnext.accounts.party import get_party_account

    return get_party_account(party_type, party, company)

@frappe.whitelist()
def get_defaults_company_currency():
    from erpnext import get_default_company

    company = get_default_company()
    
    if company:
        return company, frappe.get_cached_value("Company", company, "default_currency")

@frappe.whitelist()
def get_bank_accounts_list(filters=None):
    return frappe.db.get_list("Bank Account", filters=filters, fields="name")

@frappe.whitelist()
def get_accounts_list(filters=None):
    return frappe.db.get_list("Account", filters=filters, fields="name")

@frappe.whitelist()
def get_mode_of_payments_list(company, filters=None):
    modes = frappe.get_all("Mode of Payment", filters=filters, fields=["name"])
    result = []

    for mode in modes:
        account = frappe.get_value(
            "Mode of Payment Account",
            filters={
                "parent": mode.name,
                "company": company
            },
            fieldname="default_account"
        )

        result.append({
            "name": mode.name,
            "account": account
        })

    return result

@frappe.whitelist()
def get_employees_list(filters=None):
    return frappe.db.get_list("Employee", filters=filters, fields="name")

@frappe.whitelist()
def get_suppliers_list(filters=None):
    return frappe.db.get_list("Supplier", filters=filters, fields="name")

@frappe.whitelist()
def get_shareholders_list(filters=None):
    return frappe.db.get_list("Shareholder", filters=filters, fields="name")

@frappe.whitelist()
def get_customers_list(filters=None):
    return frappe.db.get_list("Customer", filters=filters, fields="name")

@frappe.whitelist()
def get_currencies_list(filters=None):
    return frappe.db.get_list("Currency", filters=filters, fields="name")

@frappe.whitelist()
def get_price_lists_list(filters=None):
    return frappe.db.get_list("Price List", filters=filters, fields="name")

@frappe.whitelist()
def get_uoms_list(filters=None):
    return frappe.db.get_list("UOM", filters=filters, fields="name")

@frappe.whitelist()
def get_sales_persons_list(filters=None):
    return frappe.db.get_list("Sales Person", filters=filters, fields="name")

@frappe.whitelist()
def get_sales_taxes_templates_list(filters=None):
    return frappe.db.get_list("Sales Taxes and Charges Template", filters=filters, fields="name")

@frappe.whitelist()
def get_purchase_taxes_templates_list(filters=None):
    return frappe.db.get_list("Purchase Taxes and Charges Template", filters=filters, fields="name")

@frappe.whitelist()
def get_addresses_list(filters=None):
    return frappe.db.get_list("Address", filters=filters, fields="name")

@frappe.whitelist()
def get_contacts_list(filters=None):
    return frappe.db.get_list("Contact", filters=filters, fields="name")

@frappe.whitelist()
def get_payment_terms_templates_list(filters=None):
    return frappe.db.get_list("Payment Terms Template", filters=filters, fields="name")

@frappe.whitelist()
def get_payment_terms_list(filters=None):
    return frappe.db.get_list("Payment Term", filters=filters, fields="name")

@frappe.whitelist()
def get_terms_and_conditions_list(filters=None):
    return frappe.db.get_list("Terms and Conditions", filters=filters, fields="name")

@frappe.whitelist(allow_guest=True)
def get_tax_templates():
    try:
        templates = frappe.get_all("Sales Taxes and Charges Template", fields=["name", "title"], order_by="creation desc")

        result = []
        for t in templates:
            doc = frappe.get_doc("Sales Taxes and Charges Template", t.name)
            result.append({
                "name": doc.name,
                "title": doc.title,
                "taxes": [
                    {
                        "charge_type": tax.charge_type,
                        "account_head": tax.account_head,
                        "description": tax.description,
                        "rate": tax.rate
                    } for tax in doc.taxes
                ]
            })

        return {
            "status": "success",
            "templates": result
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Tax Templates Error")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def get_cost_centers_list(filters=None):
    return frappe.db.get_list("Cost Center", filters=filters, fields="name")

@frappe.whitelist()
def get_projects_list(filters=None):
    return frappe.db.get_list("Project", filters=filters, fields="name")

@frappe.whitelist()
def get_default_country():
    try:
        default_country = frappe.db.get_single_value("System Settings", "country")
        return {
            "status": "success",
            "default_country": default_country
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Default Country Error")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def get_warehouses():
    return frappe.get_all("Warehouse", fields="name")

@frappe.whitelist()
def create_customer(customer_name, phone, address_line1, city=None, country=None):
    try:
        # Get first available Customer Group
        customer_group = frappe.get_value("Customer Group", {}, "name", order_by="creation asc")
        if not customer_group:
            return {
                "status": "error",
                "message": "No Customer Group found in the system."
            }

        # Get first available Territory
        territory = frappe.get_value("Territory", {}, "name", order_by="creation asc")
        if not territory:
            return {
                "status": "error",
                "message": "No Territory found in the system."
            }

        # If no country passed, use default from System Settings
        if not country:
            country = frappe.db.get_single_value("System Settings", "country")

        # Create the Customer
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_type": "Individual",
            "mobile_no": phone,
            "customer_group": customer_group,
            "territory": territory
        })
        customer.insert(ignore_permissions=True)

        # Create Address
        address = frappe.get_doc({
            "doctype": "Address",
            "address_title": customer_name,
            "address_type": "Billing",
            "address_line1": address_line1,
            "city": city,
            "country": country,
            "links": [{
                "link_doctype": "Customer",
                "link_name": customer.name
            }]
        })
        address.insert(ignore_permissions=True)

        return {
            "status": "success",
            "customer_id": customer.name,
            "customer_name": customer.customer_name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Customer API Error")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def get_all_customers():
    try:
        customers = frappe.get_all(
            "Customer",
            fields=["name", "customer_name", "mobile_no"],
            order_by="creation desc"
        )

        result = []
        for cust in customers:
            address = frappe.db.sql("""
                SELECT addr.address_line1, addr.city, addr.country
                FROM `tabAddress` addr
                JOIN `tabDynamic Link` dl ON dl.parent = addr.name
                WHERE dl.link_doctype = 'Customer' AND dl.link_name = %s
                LIMIT 1
            """, cust.name, as_dict=True)

            result.append({
                "customer_id": cust.name,
                "customer_name": cust.customer_name,
                "phone": cust.mobile_no,
                "address_line1": address[0].address_line1 if address else None,
                "city": address[0].city if address else None,
                "country": address[0].country if address else None
            })

        return {
            "status": "success",
            "customers": result
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get All Customers Error")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def get_items_details_list(filters=None):
    return frappe.db.get_list("Item", filters=filters, fields=["name", "item_name", "item_group", "image", "standard_rate"])


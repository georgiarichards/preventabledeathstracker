from map import DESCRIPTION_KEY, FEATURES_KEY, LOGO_PATH, PRODUCT_DETAILS_MAP, SUPPORT_EMAIL, WEBSITE_URL


def fill_email_template(customer_name, product_name) -> str:
    """
    Fills in the email template with the provided data.
    """
    product_features = PRODUCT_DETAILS_MAP[product_name][FEATURES_KEY]
    description = PRODUCT_DETAILS_MAP[product_name][DESCRIPTION_KEY]
    features_list_text = "\n".join([f"<li>{feature}</li>" for feature in product_features])
    filled_template = f"""
    <div class="container" style="max-width: 600px;margin: 20px auto;background-color: #f0f8ff;padding: 20px;border-radius: 8px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif;color: #000000">
        <img src="{LOGO_PATH}" alt="Preventable Deaths Tracker" style="max-width:100%;height:auto;">
        <h3>Thank you for choosing Preventable Deaths Tracker!</h3>
        <p>Dear {customer_name},</p>
        <p>We appreciate your recent {description}.</p>
        <p>{product_name} allows you to:</p>
        <ul>
            {features_list_text}
        </ul>
        <p>If you have any questions or need assistance, feel free to contact us at {SUPPORT_EMAIL}.</p>
        <p>Thank you again for choosing Preventable Deaths Tracker!</p>
        <a href="{WEBSITE_URL}" style="display: inline-block;padding: 10px 20px;background-color: #4CAF50;color: #ffffff;text-decoration: none;border-radius: 5px;">Explore More</a>
    </div>
    """
    return filled_template

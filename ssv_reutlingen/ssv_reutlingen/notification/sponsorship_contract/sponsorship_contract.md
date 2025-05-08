{% if doc.renew_or_expire == "Renew Automatically" %}
    The sponsorship contract is going to renew automatically on {{ doc.contract_end }}.
{% elif doc.renew_or_expire == "Expire Automatically" %}
    The sponsorship contract will expire automatically on {{ doc.contract_end }}.
{% endif %}
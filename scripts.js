// scripts.js

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function selectService(serviceId) {
    const priceElement = document.getElementById(serviceId);
    if (priceElement) {
        const selectedServiceName = priceElement.parentElement.textContent.trim().split(':')[0];
        const selectedPrice = priceElement.textContent.trim();

        document.getElementById('selectedService').textContent = selectedServiceName;
        document.getElementById('selectedPrice').textContent = selectedPrice;
        document.getElementById('completeOrderButton').disabled = false;
    } else {
        console.error(`Price element with ID '${serviceId}' not found.`);
    }
}

function completeOrder() {
    const contactId = getQueryParam('contact_id');
    if (contactId) {
        const selectedService = document.getElementById('selectedService').textContent;
        const selectedPrice = document.getElementById('selectedPrice').textContent;

        fetch(`https://property-sqft-app.onrender.com/proxy/gohighlevel/${contactId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selectedService: selectedService,
                selectedPrice: selectedPrice.replace('$', '')
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            alert('Order completed successfully!');
        })
        .catch(error => console.error('Error completing order:', error));
    } else {
        console.error('Contact ID is missing in the URL.');
    }
}

window.onload = function () {
    const contactId = getQueryParam('contact_id');
    if (contactId) {
        fetch(`https://property-sqft-app.onrender.com/proxy/gohighlevel/${contactId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Contact Data Fetched:', data);
            if (data && data.contact) {
                const contact = data.contact;
                const customFields = contact.customField || {};

                document.getElementById('one_time_mow_price').textContent = customFields.one_time_mow_price ? `$${customFields.one_time_mow_price}` : 'N/A';
                document.getElementById('recurring_maintenance_biweekly_price').textContent = customFields.recurring_maintenance_biweekly_price ? `$${customFields.recurring_maintenance_biweekly_price}` : 'N/A';
                document.getElementById('recurring_maintenance_weekly_price').textContent = customFields.recurring_maintenance_weekly_price ? `$${customFields.recurring_maintenance_weekly_price}` : 'N/A';
                document.getElementById('full_service_biweekly_price').textContent = customFields.full_service_biweekly_price ? `$${customFields.full_service_biweekly_price}` : 'N/A';
                document.getElementById('full_service_weekly_price').textContent = customFields.full_service_weekly_price ? `$${customFields.full_service_weekly_price}` : 'N/A';
                document.getElementById('weed_control_1_price').textContent = customFields.weed_control_1_price ? `$${customFields.weed_control_1_price}` : 'N/A';
                document.getElementById('weed_control_2_price').textContent = customFields.weed_control_2_price ? `$${customFields.weed_control_2_price}` : 'N/A';
                document.getElementById('weed_control_3_price').textContent = customFields.weed_control_3_price ? `$${customFields.weed_control_3_price}` : 'N/A';
            } else {
                console.error('Contact data is missing or malformed.');
            }
        })
        .catch(error => console.error('Error fetching contact data:', error));
    } else {
        console.error('Contact ID is missing in the URL.');
    }
}

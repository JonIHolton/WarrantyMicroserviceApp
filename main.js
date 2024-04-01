document.addEventListener('DOMContentLoaded', () => {
    const paymentForm = document.getElementById('paymentForm');
    paymentForm.addEventListener('submit', processPayment);
});

function processPayment(event) {
    event.preventDefault();

    // Get the values from the form inputs
    const transactionId = document.getElementById('transactionId').value;
    const amount = document.getElementById('amount').value;

    // Construct the request payload
    const paymentData = {
        transaction_id: transactionId,
        amount: amount
    };

    // Replace with the URL of your payment processing service
    const paymentServiceUrl = 'http://localhost:5000/process_payment'; 

    // Make the POST request to the payment processing service
    fetch(paymentServiceUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(paymentData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Payment processed:', data);
        // Handle successful payment processing here
        // For example, update the UI or redirect the user
    })
    .catch(error => {
        console.error('Payment processing failed:', error);
        // Handle payment processing errors here
        // For example, display an error message to the user
    });
}

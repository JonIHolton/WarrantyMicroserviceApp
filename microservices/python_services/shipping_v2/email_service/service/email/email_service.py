from postmarker.core import PostmarkClient

class EmailService:

    @staticmethod
    def send_email_via_postmark(recipient, subject, html_body, sender=None):
        try:
            # Set default values
            default_sender = "darrell.tan.2022@scis.smu.edu.sg"
            default_subject = 'ESD Rabak'
            default_text_body = "Hello, this is a test email sent via Postmark."
            default_html_body = "<html><body><p>Hello, this is a test email sent via Postmark.</p></body></html>"

            # Use provided values or defaults
            sender_email = sender if sender else default_sender
            email_subject = subject if subject else default_subject
            email_html_body = html_body if html_body else default_html_body

            # Your Postmark server token
            token = "5200ad5e-6357-4739-9c62-36bf526301fc"

            # Initialize the Postmark client
            client = PostmarkClient(server_token=token)

            # Send the email
            # client.emails.send(
            #     From=sender_email,
            #     To=recipient,
            #     Subject=email_subject,
            #     HtmlBody=email_html_body,
            # )

            print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
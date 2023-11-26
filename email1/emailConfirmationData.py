def create_subject_body(name, link):
     subject = "Confirm Your Email Address"
     body = f"""Hello {name},
 Thank you for signing up for our service! We're excited to have you on board. Before you can start using your account, we just need to confirm your email address.
 To confirm your email address, please click on the following link:
 {link}
 If you didn't sign up for our service, please disregard this email.
 Thank you,
     FlashBrain"""

     return subject, body
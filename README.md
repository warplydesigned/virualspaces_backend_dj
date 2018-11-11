# virualspaces_backend_dj
Backend Django API for Virtual Spaces Project

# Account management (djoser)
1. Create account - POST
    - /api/user/create/
    - Required data:
        - email
        - password
    - Returns email and id confirming the account was created, call Login api to actually login. and get 

2. Account details - GET
    - /api/user/view/
    - Headers: 'Authorization: JWT token_from_login_step_1'
    - Returns id, email

3. Logout all logged in devices for an account
    - /api/user/logout/all/
    - Headers: 'Authorization: JWT token_from_login_step_1'

4. Delete logged in user
    - /api/user/delete/
    - Headers: 'Authorization: JWT token_from_login_step_1'
    - Required
        - current_password sent as data

5. Reset password - POST (TODO: Change email template)
    - /api/user/password/reset/
    - Required
        - email
    - Sends email with uid and token needed to change password in next step

6. Password reset confirm - POST
    - /api/user/password/reset/confirm/
    - Required
        - uid (emailed in step 5)
        - token (emailed in step 5)
        - new_password
    - Returns 204

7. Change password - POST
    - /api/user/password/change/
    - Headers: 'Authorization: JWT token_from_login_step_1'
    - Required
        - current_password
        - new_password
    - Returns 204

# Steps to verify devices (2 step authentication via django_otp)
1. Login - POST
    - /api/user/login/ requires email and password
    - Will return autorization token need for next request.

2. Create TOTP secret (only done once per device unless deleted) - GET
    - /api/totp/create/
    - Headers: 'Authorization: JWT token_from_step_1'
    - Will return a url which can be used to generate barcode, or
    you can use the secret + email in step 1 to setup google authenticator.
    Where secret is the key and account is the email.

3. Verify device - POST
    - /api/totp/login/numbers_from_google_authenticator/ *Do not include the spaces*
    - Headers: 'Authorization: JWT token_from_step_1'
    - Will return a new token that will replace the one in step 1, use this from now on.
    - Once a device has been verified you will always need to use this second level
    login. (Heince the 2 step :))
    - NOTE: If a device has not been verified you don't need to follow two step auth.

4. Add otp.permissions.IsOtpVerified to the permission_classes of all rest views where
you want protected by 2 step authentication. This will give access deined to users who
don't use step 3 to get a new token for already verified devices.

5. Generate emergancy codes for a verified device. - GET
    - First perform steps 1 and 3
    - /api/static/create/
    - Headers: 'Authorization: JWT token_from_step_3'
    - Will return 6 one time use emergancy tokens, use this if you don't have access to
    the verified device that has google authenticator.

6. Use emergancy codes - GET
    - Perform step 1
    - /api/static/login/5xaov5f5/
    - Headers: 'Authorization: JWT token_from_step_1'
    - Will return a new token use this from now on in the Headers

7. Delete a verified device (normally only used if you don't have access to the device) - POST
    - Perform step 1
    - Perform step 6 with one of the saved not used codes
    - /api/totp/delete/
    - Headers: 'Authorization: JWT token_from_step_6'
    - Will return new token use this from now on in the Headers

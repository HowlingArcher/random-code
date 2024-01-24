import qrcode

def generate_qr_code(url):
    # Create instance of QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the instance
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save("qrcode.png")

if __name__ == "__main__":
    # Get URL from user input
    url = input("Enter the URL for the QR Code: ")

    # Generate QR Code
    generate_qr_code(url)

    print("QR Code generated successfully!")
const appointmentForm =
    document.getElementById("appointmentForm");

const formMessage =
    document.getElementById("formMessage");

const submitButton =
    document.getElementById("submitButton");


appointmentForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // Get values from the form

        const name =
            document
                .getElementById("name")
                .value
                .trim();


        const phone =
            document
                .getElementById("phone")
                .value
                .trim();


        const service =
            document
                .getElementById("service")
                .value;


        const location =
            document
                .getElementById("location")
                .value;


        const message =
            document
                .getElementById("message")
                .value
                .trim();


        // Create appointment data

        const appointmentData = {

            name: name,

            phone: phone,

            service: service,

            location: location,

            message: message

        };


        try {

            // Disable button while submitting

            submitButton.disabled = true;

            submitButton.innerText =
                "Booking Appointment...";

            formMessage.innerText = "";


            // Send data to FastAPI backend

            const response = await fetch(
                "/appointments",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        appointmentData
                    )

                }
            );


            // Check if request failed

            if (!response.ok) {

                throw new Error(
                    "Failed to book appointment"
                );

            }


            // Get response from backend

            const result =
                await response.json();


            // Show success message

            formMessage.style.color =
                "#2ee7e2";

            formMessage.innerText =
                "✓ Appointment booked successfully! We will contact you soon.";


            console.log(
                "Appointment saved:",
                result
            );


            // Clear form

            appointmentForm.reset();


        }

        catch (error) {

            console.error(
                "Appointment error:",
                error
            );


            formMessage.style.color =
                "#ff7777";

            formMessage.innerText =
                "Something went wrong. Please try again or call us at 9889140864.";

        }

        finally {

            // Enable button again

            submitButton.disabled = false;

            submitButton.innerText =
                "Book Appointment";

        }

    }
);
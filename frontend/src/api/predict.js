
const API_URL = import.meta.env.VITE_API_URL

export const predictChurn = async (customerData) => {
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(customerData)
        })

        if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || "Prediction failed")
        }

        const data = await response.json()
        return data

    } catch (error) {
        throw new Error(error.message || "Something went wrong")
    }
}
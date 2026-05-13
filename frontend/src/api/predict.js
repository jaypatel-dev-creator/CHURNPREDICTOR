import axios from "axios"
// .meta.env is react's mechanism for importing environment files 
const API_URL = import.meta.env.VITE_API_URL 

export const predictChurn = async (customerData) => {
    try {
        const response = await axios.post(`${API_URL}/predict`, customerData)
        return response.data

    } catch (error) {
        throw new Error(error.response?.data?.detail || "Prediction failed")
    }
}
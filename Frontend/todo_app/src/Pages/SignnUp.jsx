import { useState } from "react";
import api from "./api/index";

function SignnUp() {
    const [form, SetForm] = useState({
        email: "",
        name: "",
        password: ""
    })

    const [message, setMessage] = useState("")

    function handleChange(e) {
        SetForm({...form, [e.target.name]: [e.target.value]})
    }

    async function handleSubmit(e) {
        e.preventDefault();
        const res = await api.post('/signup', form)
        if (res.ok) {
            setMessage("Sign up successful")
        } 
    }

    return(
        <div>
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input type="text" onChange={handleChange} placeholder="Enter your name" />
                </div>

                <div>
                    <label>Email:</label>
                    <input type="email" onChange={handleChange} placeholder="Enter your email" />
                </div>

                <label>Password:</label>
                <input type="password" onChange={handleChange} placeholder="Enter your password" />

                <button type="submit">
                    Sign up
                </button>
            </form>
        </div>
    )
}

export default SignnUp
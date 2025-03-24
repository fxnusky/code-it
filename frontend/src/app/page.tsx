"use client"
import styles from "./page.module.css";
import { useState, useEffect } from "react";
import SetupService from "../../sevices/setup.service";
import Login from "../../sevices/authentication.service";


export default function Home() {
    const [text, setText] = useState(""); 
    const [user, setUser] = useState<any>(null);

    const handleLoginSuccess = (user: any) => {
        setUser(user);
    };

    const handleLogout = () => {
        localStorage.removeItem('google_token');
        setUser(null);
    };

    useEffect(() => {
        SetupService.getText().then((fetchedText: string) => {
            if (fetchedText !== null) {
                setText(fetchedText); 
            }
        });
    }, []); 

    return (
        <div className={styles.page}>
            {text}
            {user ? (
                <div>
                    <p>Hello, {user.name}!</p>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <Login onLoginSuccess={handleLoginSuccess} />
            )}
        </div>
    );
}

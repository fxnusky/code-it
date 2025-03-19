"use client"
import styles from "./page.module.css";
import { useState, useEffect } from "react";
import SetupService from "../../sevices/setup.service";


export default function Home() {
    const [text, setText] = useState(""); 

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
        </div>
    );
}

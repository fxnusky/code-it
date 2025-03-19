import endpoint from "../endpoints.config";

const SetupService = {
    getText: async () => {
        try {
            const response = await fetch(endpoint.dbURL + "/");

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data.text; 
        } catch (error) {
            console.error("Failed to fetch text:", error);
            return null;
        }
    }

};

export default SetupService;
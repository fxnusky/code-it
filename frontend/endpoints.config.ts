const endpoint = {
    dbURL: process.env.NEXT_PUBLIC_API_DB_URL || '', 
    isolateURL: process.env.NEXT_PUBLIC_ISOLATE_API_DB_URL || '', 
    wsURL: process.env.NEXT_PUBLIC_WS_API_DB_URL || '', 
  };
  
  export default endpoint;
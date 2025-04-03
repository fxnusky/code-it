import "./globals.css";
import { AuthProvider } from "../../contexts/auth_context";
import { WSProvider } from "../../contexts/ws_connection_context";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html data-lt-installed="true" suppressHydrationWarning>
      <body >
        <WSProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </WSProvider>
      </body>
    </html>
  );
}

import "./globals.css";
import { AuthProvider } from "../../contexts/auth_context";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html data-lt-installed="true" suppressHydrationWarning>
      <body >
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

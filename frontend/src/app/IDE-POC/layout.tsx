import "../globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html data-lt-installed="true">
      <body >
        {children}
      </body>
    </html>
  );
}

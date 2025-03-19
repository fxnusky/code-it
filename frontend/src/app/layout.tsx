import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html data-lt-installed="true" suppressHydrationWarning>
      <body >
        <div>Layout</div>
        {children}
      </body>
    </html>
  );
}

import 'bootstrap/dist/css/bootstrap.css';
import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';



const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Simp!Law',
  description: 'Swiss Legal Advise - Simplefied',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="chat-container">
          <div className="chat-header">simp!LAW</div>
            <div>{children}</div>
        </div>
      </body>
    </html>

  );
}

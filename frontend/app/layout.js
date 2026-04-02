export const metadata = {
  title: 'AI算力匹配桥',
  description: '连接闲置GPU与AI推理需求',
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <body>{children}</body>
    </html>
  )
}

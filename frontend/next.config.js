/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["@aioia/core"],
  async redirects() {
    return [
      {
        source: "/",
        destination: "/en",
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;

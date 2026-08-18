import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  basePath: process.env.GITHUB_PAGES === "true" ? "/MDfy" : "",
  assetPrefix: process.env.GITHUB_PAGES === "true" ? "/MDfy/" : "",
  images: { unoptimized: true },
};

export default nextConfig;

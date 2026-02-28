import { type NextRequest, NextResponse } from "next/server";

export async function middleware(_request: NextRequest) {
  // No authentication middleware — all routes are public
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};

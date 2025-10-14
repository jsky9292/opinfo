
import type { RouteObject } from "react-router-dom";
import NotFound from "../pages/NotFound";
import Home from "../pages/home/page";
import ShopDetail from "../pages/shop-detail/page-simple";
import Login from "../pages/auth/login";
import Signup from "../pages/auth/signup";
import AdminDashboard from "../pages/admin/dashboard";
import TestLogin from "../pages/test-login";

const routes: RouteObject[] = [
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/shop/:id",
    element: <ShopDetail />,
  },
  {
    path: "/auth/login",
    element: <Login />,
  },
  {
    path: "/auth/signup",
    element: <Signup />,
  },
  {
    path: "/admin",
    element: <AdminDashboard />,
  },
  {
    path: "/admin/dashboard",
    element: <AdminDashboard />,
  },
  {
    path: "/test-login",
    element: <TestLogin />,
  },
  {
    path: "*",
    element: <NotFound />,
  },
];

export default routes;

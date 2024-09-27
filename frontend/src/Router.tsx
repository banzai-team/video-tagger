// import React from "react";
import {BrowserRouter, Link, RouteObject, useRoutes} from "react-router-dom";
import MainLayout from "@/components/MainLayout";
import NewVideoPage from "@/pages/NewVideoPage";
import MainPage from "@/pages/MainPage";
import {ArrowLeft} from "lucide-react";
import EmptyView from "@/components/EmptyView";

export const Routes = {
    Root: '/',
    Video: '/video',
    New: '/new',
};

const InnerRouter = () => {
    const routes: RouteObject[] = [
        {
            path: '/',
            element: <MainLayout />,
            children: [
                {
                    index: true,
                    element: <MainPage/>,
                },
                {
                    path: Routes.New,
                    element: <NewVideoPage/>,
                },
                {
                    path: `${Routes.Video}/:id`,
                    element: <h2>Video # ????</h2>,
                },
                {
                    path: "*",
                    element: (
                        <EmptyView title="404" description="такой страницы не существует">
                            <Link
                                className="flex gap-2 items-center hover:opacity-80 "
                                to={Routes.Root}
                            >
                                <ArrowLeft className="h-5 w-5"/>вернуться на главную</Link>
                        </EmptyView>
                    ),

                },
            ],
        },
    ];
    return useRoutes(routes);
};

export const Router = () => {
    return (
        <BrowserRouter>
            <InnerRouter />
        </BrowserRouter>
    );
};
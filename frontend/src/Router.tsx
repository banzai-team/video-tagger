// import React from "react";
import {BrowserRouter, RouteObject, useRoutes} from "react-router-dom";
import MainLayout from "@/components/MainLayout";
import NewVideoPage from "@/pages/NewVideoPage";

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
                    element: <h2>Ваши видео</h2>,
                },
                {
                    path: Routes.New,
                    element: <NewVideoPage/>,
                },
                {
                    path: `${Routes.Video}/:id`,
                    element: <h2>Выбранное видео</h2>,
                },
                {
                    path: "*",
                    element: <h2>404</h2>,
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
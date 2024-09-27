// import React from "react";
import {BrowserRouter, RouteObject, useRoutes} from "react-router-dom";
import MainLayout from "@/components/MainLayout";

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
                    element: <div>Ваши видео</div>,
                },
                {
                    path: Routes.New,
                    element: <div>Добавить видео</div>,
                },
                {
                    path: `${Routes.Video}/:id`,
                    element: <div>Выбранное видео</div>,
                },
                {
                    path: "*",
                    element: <div>404</div>,
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
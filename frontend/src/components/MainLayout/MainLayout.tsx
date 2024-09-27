import React from 'react';
import { Outlet } from 'react-router-dom';
import {Home, PlusCircle} from "lucide-react";

import Sidebar from "@/components/MainLayout/components/Sidebar.tsx";
import Header from "@/components/MainLayout/components/Header.tsx";

export type MenuItemsType = {
    text: string;
    link: string;
    icon: string | React.ReactNode;
};

const menuItems = [
    {
        text: "Добавить видео",
        icon: <PlusCircle className="h-5 w-5" />,
        link: "new",
    },
    {
        text: "Главная",
        icon: <Home className="h-5 w-5" />,
        link: "/"
    },
];

const MainLayout: React.FC = () => {
    return (
        <div
            className="flex min-h-screen w-full flex-col bg-white bg-center bg-no-repeat bg-cover"
            style={{backgroundImage: 'url(/bg.svg)'}}
        >
            <Sidebar menuItems={menuItems} />
            <div className="flex flex-col sm:gap-4 sm:py-4 sm:pl-52">
                <Header menuItems={menuItems} />
                <main className="flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8 lg:grid-cols-3 xl:grid-cols-3">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default MainLayout;

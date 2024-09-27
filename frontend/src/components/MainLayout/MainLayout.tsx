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
            className="flex min-h-screen h-screen w-full flex-col bg-center bg-no-repeat bg-cover
                {/*bg-white*/}
                bg-sidebar
            "
            style={{backgroundImage: 'url(/bg.svg)'}}
        >
            <Sidebar menuItems={menuItems} />
            <div className="flex flex-col h-full w-full sm:pl-60 sm:py-4 sm:pr-4">
                <Header menuItems={menuItems} />
                <main
                    className="flex-1 items-start
                        bg-white  h-full w-full
                        p-4 sm:px-10 sm:py-4
                        sm:rounded-3xl
                        "
                >
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default MainLayout;

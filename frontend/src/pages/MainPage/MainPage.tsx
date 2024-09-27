import React from 'react';
import EmptyView from "@/components/EmptyView";
import {Button} from "@/components/ui/button.tsx";
import {Plus} from "lucide-react";
import {useNavigate} from "react-router-dom";
import {Routes} from "@/Router.tsx";

const MainPage: React.FC = () => {
    const navigate = useNavigate();

    const data = [];

    return (
        <>
            <h2>Ваши видео</h2>
            {
                !data || !data.length
                ? (<EmptyView title="Список видео пуст">
                        <Button
                            className="flex gap-2"
                            onClick={() => navigate(Routes.New)}
                        >
                            <Plus className=""/>Добавить видео</Button>
                    </EmptyView>)
                : <div>table</div>
            }
        </>
    );
};

export default MainPage;

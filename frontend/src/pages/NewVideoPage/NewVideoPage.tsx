import React from 'react';
import AddVideoForm from "@/pages/NewVideoPage/components/AddVideoForm.tsx";

const NewVideoPage: React.FC = () => {
    return (
        <>
            <h2>Добавить новое видео</h2>
            <h4 className="mb-10">Вы можете добавить id/ссылку на видео или загрузить видео файл с описанием</h4>
            <div>
                <AddVideoForm/>
            </div>
        </>
    );
};

export default NewVideoPage;

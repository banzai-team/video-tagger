import React from 'react';
import AddVideoForm from "@/pages/NewVideoPage/components/AddVideoForm.tsx";
import {
  useInferenceEndpointsServiceProcessVideoUrlV1ProcessVideoUrlPost,
  useInferenceEndpointsServiceProcessVideoFileV1ProcessVideoFilePost
} from "@/openapi/queries/queries";
import { useNavigate } from 'react-router-dom';
import { Routes } from '@/Router';

const NewVideoPage: React.FC = () => {
  const navigate = useNavigate()

  const redirectFunc = (data) => {
    setTimeout(() => {
      navigate(`${Routes.Video}/${data?.video_id}`)
    }, 1500)
  }

  const { mutate: mutateUrl } = useInferenceEndpointsServiceProcessVideoUrlV1ProcessVideoUrlPost({
    onSuccess: (data) => {
      redirectFunc(data)
    },
  });

  const { mutate: mutateFile } = useInferenceEndpointsServiceProcessVideoFileV1ProcessVideoFilePost({
    onSuccess: (data) => {
      redirectFunc(data)
    },
  });

  const onSubmit = async (values) => {
    if (values.link) mutateUrl({ requestBody: { video_url: values.link } })
    else mutateFile({ formData: { file: values.files, description: values.description, title: values.title } })
  }

  return (
    <>
      <h2>Добавить новое видео</h2>
      <h4 className="mb-10">Вы можете добавить id/ссылку на видео или загрузить видео файл с описанием</h4>
      <div>
        <AddVideoForm onSubmit={onSubmit} />
      </div>
    </>
  );
};

export default NewVideoPage;

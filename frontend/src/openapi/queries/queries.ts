// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { UseMutationOptions, UseQueryOptions, useMutation, useQuery } from "@tanstack/react-query";
import { InferenceEndpointsService, SystemProbsService } from "../requests/services.gen";
import { Body_process_video_file_v1_process_video_file_post, VideoUrlInput } from "../requests/types.gen";
import * as Common from "./common";
export const useInferenceEndpointsServiceGetVideoByIdV1VideosIdGet = <TData = Common.InferenceEndpointsServiceGetVideoByIdV1VideosIdGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>({ id }: {
  id: unknown;
}, queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useQuery<TData, TError>({ queryKey: Common.UseInferenceEndpointsServiceGetVideoByIdV1VideosIdGetKeyFn({ id }, queryKey), queryFn: () => InferenceEndpointsService.getVideoByIdV1VideosIdGet({ id }) as TData, ...options });
export const useInferenceEndpointsServiceGetVideosV1VideosGet = <TData = Common.InferenceEndpointsServiceGetVideosV1VideosGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>({ size, skip }: {
  size?: unknown;
  skip?: unknown;
} = {}, queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useQuery<TData, TError>({ queryKey: Common.UseInferenceEndpointsServiceGetVideosV1VideosGetKeyFn({ size, skip }, queryKey), queryFn: () => InferenceEndpointsService.getVideosV1VideosGet({ size, skip }) as TData, ...options });
export const useSystemProbsServiceHealthHealthGet = <TData = Common.SystemProbsServiceHealthHealthGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>(queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useQuery<TData, TError>({ queryKey: Common.UseSystemProbsServiceHealthHealthGetKeyFn(queryKey), queryFn: () => SystemProbsService.healthHealthGet() as TData, ...options });
export const useInferenceEndpointsServiceProcessVideoUrlV1ProcessVideoUrlPost = <TData = Common.InferenceEndpointsServiceProcessVideoUrlV1ProcessVideoUrlPostMutationResult, TError = unknown, TContext = unknown>(options?: Omit<UseMutationOptions<TData, TError, {
  requestBody: VideoUrlInput;
}, TContext>, "mutationFn">) => useMutation<TData, TError, {
  requestBody: VideoUrlInput;
}, TContext>({ mutationFn: ({ requestBody }) => InferenceEndpointsService.processVideoUrlV1ProcessVideoUrlPost({ requestBody }) as unknown as Promise<TData>, ...options });
export const useInferenceEndpointsServiceProcessVideoFileV1ProcessVideoFilePost = <TData = Common.InferenceEndpointsServiceProcessVideoFileV1ProcessVideoFilePostMutationResult, TError = unknown, TContext = unknown>(options?: Omit<UseMutationOptions<TData, TError, {
  formData: Body_process_video_file_v1_process_video_file_post;
}, TContext>, "mutationFn">) => useMutation<TData, TError, {
  formData: Body_process_video_file_v1_process_video_file_post;
}, TContext>({ mutationFn: ({ formData }) => InferenceEndpointsService.processVideoFileV1ProcessVideoFilePost({ formData }) as unknown as Promise<TData>, ...options });

// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { UseMutationOptions, UseQueryOptions, useMutation, useQuery } from "@tanstack/react-query";
import { InferenceEndpointsService, SystemProbsService, VideoManagementService } from "../requests/services.gen";
import { Body_process_video_file_v1_process_video_file_post, VideoUrlInput } from "../requests/types.gen";
import * as Common from "./common";
export const useVideoManagementServiceListVideosV1ListVideosGet = <TData = Common.VideoManagementServiceListVideosV1ListVideosGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>(queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useQuery<TData, TError>({ queryKey: Common.UseVideoManagementServiceListVideosV1ListVideosGetKeyFn(queryKey), queryFn: () => VideoManagementService.listVideosV1ListVideosGet() as TData, ...options });
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

import type React from 'react'
import { useState } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from '@/components/ui/sonner'
import TextPostTab from './TextPostTab'
import AudioPostTab from './AudioPostTab'
import VideoPostTab from './VideoPostTab'
import MediaPreview from './MediaPreview'
import type { CreatePostRequest } from '@/types/post'

interface CreatePostProps {
	onPostCreated: (post: CreatePostRequest) => void
}

const getMediaExtension = (mimeType: string, mediaType: 'audio' | 'video'): string => {
	const baseType = mimeType.split(';')[0] // Remove codec information
	if (mediaType === 'audio') {
		return baseType === 'audio/webm'
			? 'webm'
			: baseType === 'audio/mp4'
				? 'm4a'
				: baseType === 'audio/ogg'
					? 'ogg'
					: 'webm' // Default to webm as it's most widely supported
	}
	return baseType === 'video/webm'
		? 'webm'
		: baseType === 'video/mp4'
			? 'mp4'
			: baseType === 'video/ogg'
				? 'ogg'
				: 'webm' // Default to webm as it's most widely supported
}

const CreatePost: React.FC<CreatePostProps> = ({ onPostCreated }) => {
	const [postText, setPostText] = useState('')
	const [mediaType, setMediaType] = useState<'text' | 'audio' | 'video'>('text')
	const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
	const [videoBlob, setVideoBlob] = useState<Blob | null>(null)
	const [audioFile, setAudioFile] = useState<File | null>(null)
	const [videoFile, setVideoFile] = useState<File | null>(null)

	const handlePostTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
		setPostText(e.target.value)
	}

	const handleAudioCaptured = (blob: Blob) => {
		setAudioBlob(blob)
		setMediaType('audio')
	}

	const handleVideoCaptured = (blob: Blob) => {
		setVideoBlob(blob)
		setVideoFile(null)
		setMediaType('video')
	}

	const handleAudioFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0]
		if (file?.type.startsWith('audio/')) {
			setAudioFile(file)
			setAudioBlob(null)
			setMediaType('audio')
		} else if (file) {
			toast.error('Please select a valid audio file')
		}
	}

	const handleVideoFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0]
		if (file?.type.startsWith('video/')) {
			setVideoFile(file)
			setVideoBlob(null)
			setMediaType('video')
		} else if (file) {
			toast.error('Please select a valid video file')
		}
	}

	const clearMedia = () => {
		setAudioBlob(null)
		setVideoBlob(null)
		setAudioFile(null)
		setVideoFile(null)
		setMediaType('text')
	}

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()

		if (!postText.trim() && !audioBlob && !audioFile && !videoBlob && !videoFile) {
			toast.error('Please enter some text or add media')
			return
		}

		let finalMediaType: 'audio' | 'video' | undefined
		let file: File | null = null

		if (mediaType === 'audio' && (audioBlob || audioFile)) {
			const blob = audioFile || audioBlob
			if (blob) {
				finalMediaType = 'audio'
				if (!(blob instanceof File)) {
					const extension = getMediaExtension(blob.type, 'audio')
					file = new File([blob], `recording_${Date.now()}.${extension}`, { type: blob.type })
				} else {
					file = blob
				}
			}
		} else if (mediaType === 'video' && (videoBlob || videoFile)) {
			const blob = videoFile || videoBlob
			if (blob) {
				finalMediaType = 'video'
				if (!(blob instanceof File)) {
					const extension = getMediaExtension(blob.type, 'video')
					file = new File([blob], `recording_${Date.now()}.${extension}`, { type: blob.type })
				} else {
					file = blob
				}
			}
		}

		const newPost: CreatePostRequest = {
			text: postText,
			media_type: finalMediaType,
			media: file,
		}

		onPostCreated(newPost)

		// Reset form
		setPostText('')
		clearMedia()

		toast.success('Post created successfully!')
	}

	const handleTabSubmit = () => {
		handleSubmit({ preventDefault: () => {} } as React.FormEvent)
	}

	return (
		<div className="bg-card rounded-lg shadow-xs p-4 border">
			<form onSubmit={handleSubmit}>
				<Textarea
					placeholder="What's happening?"
					value={postText}
					onChange={handlePostTextChange}
					className="w-full resize-none mb-4 border-none focus-visible:ring-0 py-2 px-3 text-base"
				/>

				<MediaPreview
					mediaType={mediaType}
					audioBlob={audioBlob}
					audioFile={audioFile}
					videoBlob={videoBlob}
					videoFile={videoFile}
					onClearMedia={clearMedia}
				/>

				<Tabs defaultValue="text" value={mediaType} className="mt-2">
					<TabsList className="grid w-full grid-cols-3 mb-4">
						<TabsTrigger value="text" onClick={() => setMediaType('text')}>
							Text
						</TabsTrigger>
						<TabsTrigger value="audio" onClick={() => setMediaType('audio')}>
							Audio
						</TabsTrigger>
						<TabsTrigger value="video" onClick={() => setMediaType('video')}>
							Video
						</TabsTrigger>
					</TabsList>

					<TabsContent value="text">
						<TextPostTab onSubmit={handleTabSubmit} />
					</TabsContent>

					<TabsContent value="audio">
						<AudioPostTab
							onAudioCaptured={handleAudioCaptured}
							onAudioFileChange={handleAudioFileChange}
							onSubmit={handleTabSubmit}
						/>
					</TabsContent>

					<TabsContent value="video">
						<VideoPostTab
							onVideoCaptured={handleVideoCaptured}
							onVideoFileChange={handleVideoFileChange}
							onSubmit={handleTabSubmit}
						/>
					</TabsContent>
				</Tabs>
			</form>
		</div>
	)
}

export default CreatePost

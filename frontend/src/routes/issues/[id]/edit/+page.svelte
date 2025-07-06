<!-- src/routes/issues/[id]/edit/+page.svelte -->
<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	
	let issue = null;
	let title = '';
	let description = '';
	let status = 'OPEN';
	let isLoading = true;
	let isSaving = false;
	let error = '';

	$: issueId = $page.params.id;

	onMount(async () => {
		if (browser && issueId) {
			await loadIssue();
		}
	});

	async function loadIssue() {
		try {
			const token = localStorage.getItem('access_token');
			const response = await fetch(`http://localhost:8000/issues/`, {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			});

			if (response.ok) {
				const issues = await response.json();
				issue = issues.find(i => i.id === issueId);
				if (issue) {
					title = issue.title;
					description = issue.description || '';
					status = issue.status;
				} else {
					error = 'Issue not found';
				}
			} else {
				error = 'Failed to load issue';
			}
		} catch (err) {
			error = 'Network error. Please try again.';
		} finally {
			isLoading = false;
		}
	}

	async function handleSubmit(event) {
		event.preventDefault();
		isSaving = true;
		error = '';

		try {
			const token = localStorage.getItem('access_token');
			const response = await fetch(`http://localhost:8000/issues/${issueId}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					title,
					description,
					status
				})
			});

			if (response.ok) {
				goto(`/issues/${issueId}`);
			} else {
				const data = await response.json();
				error = data.detail || 'Failed to update issue';
			}
		} catch (err) {
			error = 'Network error. Please try again.';
		} finally {
			isSaving = false;
		}
	}

	function getStatusColor(status) {
		switch (status) {
			case 'OPEN': return 'bg-red-100 text-red-800';
			case 'IN_PROGRESS': return 'bg-yellow-100 text-yellow-800';
			case 'RESOLVED': return 'bg-green-100 text-green-800';
			case 'CLOSED': return 'bg-gray-100 text-gray-800';
			default: return 'bg-gray-100 text-gray-800';
		}
	}

	function formatStatus(status) {
		return status.replace('_', ' ');
	}
</script>

<svelte:head>
	<title>Edit Issue - Issue Tracker</title>
</svelte:head>

<div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
	{#if isLoading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
		</div>
	{:else if error}
		<div class="text-center py-12">
			<div class="text-red-600 mb-4">
				<svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
				</svg>
			</div>
			<h3 class="text-lg font-medium text-gray-900 mb-2">Error</h3>
			<p class="text-gray-600 mb-4">{error}</p>
			<a href="/issues" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
				Back to Issues
			</a>
		</div>
	{:else}
		<!-- Breadcrumb -->
		<div class="mb-8">
			<nav class="flex" aria-label="Breadcrumb">
				<ol class="flex items-center space-x-4">
					<li>
						<div>
							<a href="/issues" class="text-gray-400 hover:text-gray-500">
								<svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
								</svg>
								<span class="sr-only">Back</span>
							</a>
						</div>
					</li>
					<li>
						<div class="flex items-center">
							<svg class="h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
						</svg>
						<a href="/issues" class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700">Issues</a>
					</div>
				</li>
				<li>
					<div class="flex items-center">
						<svg class="h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
						</svg>
						<a href="/issues/{issueId}" class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700">#{issueId.split('-')[0]}</a>
					</div>
				</li>
				<li>
					<div class="flex items-center">
						<svg class="h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
						</svg>
						<span class="ml-4 text-sm font-medium text-gray-500">Edit</span>
					</div>
				</li>
			</ol>
		</nav>
		
		<h1 class="mt-4 text-3xl font-bold text-gray-900">Edit Issue</h1>
		<p class="mt-2 text-gray-600">Update issue details and status</p>
	</div>

	<div class="bg-white shadow-sm rounded-lg border border-gray-200">
		<form on:submit={handleSubmit} class="space-y-6 p-6">
			<div>
				<label for="title" class="block text-sm font-medium text-gray-700 mb-2">
					Issue Title *
				</label>
				<input
					id="title"
					name="title"
					type="text"
					required
					bind:value={title}
					placeholder="Brief description of the issue"
					class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
				/>
			</div>

			<div>
				<label for="description" class="block text-sm font-medium text-gray-700 mb-2">
					Description
				</label>
				<textarea
					id="description"
					name="description"
					rows="6"
					bind:value={description}
					placeholder="Detailed description of the issue..."
					class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
				></textarea>
			</div>

			<div>
				<label for="status" class="block text-sm font-medium text-gray-700 mb-2">
					Status
				</label>
				<select
					id="status"
					name="status"
					bind:value={status}
					class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
				>
					<option value="OPEN">Open</option>
					<option value="IN_PROGRESS">In Progress</option>
					<option value="RESOLVED">Resolved</option>
					<option value="CLOSED">Closed</option>
				</select>
				<div class="mt-2 flex items-center space-x-2">
					<span class="text-sm text-gray-500">Current status:</span>
					<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(status)}">
						{formatStatus(status)}
					</span>
				</div>
			</div>

			{#if error}
				<div class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
					{error}
				</div>
			{/if}

			<div class="flex items-center justify-between pt-4 border-t border-gray-200">
				<a href="/issues/{issueId}" 
				   class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors">
					Cancel
				</a>
				<button
					type="submit"
					disabled={isSaving || !title.trim()}
					class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					{#if isSaving}
						<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
					{/if}
					{isSaving ? 'Saving...' : 'Save Changes'}
				</button>
			</div>
		</form>
	</div>

	<!-- Issue Info -->
	{#if issue}
		<div class="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
			<h3 class="text-sm font-medium text-gray-900 mb-2">Issue Information</h3>
			<dl class="grid grid-cols-1 gap-x-4 gap-y-2 sm:grid-cols-2 text-sm">
				<div>
					<dt class="font-medium text-gray-500">Issue ID:</dt>
					<dd class="text-gray-900 font-mono">{issue.id}</dd>
				</div>
				<div>
					<dt class="font-medium text-gray-500">Created:</dt>
					<dd class="text-gray-900">{new Date(issue.created_at).toLocaleDateString()}</dd>
				</div>
				<div>
					<dt class="font-medium text-gray-500">Created By:</dt>
					<dd class="text-gray-900">{issue.created_by || 'Unknown'}</dd>
				</div>
				{#if issue.updated_at && issue.updated_at !== issue.created_at}
					<div>
						<dt class="font-medium text-gray-500">Last Updated:</dt>
						<dd class="text-gray-900">{new Date(issue.updated_at).toLocaleDateString()}</dd>
					</div>
				{/if}
			</dl>
		</div>
	{/if}
	{/if}
</div>
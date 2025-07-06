<script lang="ts">
	let title = '';
	let description = '';
	let priority = 'LOW';

	const createIssue = async () => {
		const token = localStorage.getItem('access_token');
		const res = await fetch('http://localhost:8000/api/issues', {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ title, description, priority }),
		});

		if (res.ok) {
			alert('Issue created');
			window.location.href = '/dashboard';
		} else {
			alert('Failed to create issue');
		}
	};
</script>

<h2 class="text-2xl font-bold mb-4">Create New Issue</h2>

<div class="space-y-4 max-w-md">
	<input class="border p-2 w-full rounded" bind:value={title} placeholder="Issue title" />
	<textarea class="border p-2 w-full rounded" bind:value={description} placeholder="Description"></textarea>
	<select class="border p-2 w-full rounded" bind:value={priority}>
		<option value="LOW">Low</option>
		<option value="MEDIUM">Medium</option>
		<option value="HIGH">High</option>
	</select>
	<button on:click={createIssue} class="bg-blue-600 text-white p-2 rounded">Submit</button>
</div>

<!-- frontend/src/lib/components/Chart.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';
    
    export let data: Array<{ label: string; value: number; color?: string }> = [];
    export let type: 'bar' | 'doughnut' | 'line' = 'bar';
    export let height: string = '400';
    export let title: string = '';
    
    let canvas: HTMLCanvasElement;
    let chart: any = null;
    
    onMount(async () => {
      if (!browser) return;
      
      // Dynamically import Chart.js to avoid SSR issues
      const { Chart, registerables } = await import('chart.js');
      Chart.register(...registerables);
      
      createChart(Chart);
    });
    
    $: if (chart && data) {
      updateChart();
    }
    
    function createChart(Chart: any) {
      if (!canvas || !data.length) return;
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      const chartConfig = getChartConfig();
      chart = new Chart(ctx, chartConfig);
    }
    
    function updateChart() {
      if (!chart) return;
      
      chart.data = getChartData();
      chart.update();
    }
    
    function getChartConfig() {
      return {
        type,
        data: getChartData(),
        options: getChartOptions()
      };
    }
    
    function getChartData() {
      const labels = data.map(item => item.label);
      const values = data.map(item => item.value);
      const colors = data.map(item => item.color || getDefaultColor());
      
      return {
        labels,
        datasets: [{
          label: title || 'Data',
          data: values,
          backgroundColor: type === 'doughnut' ? colors : colors.map(color => `${color}20`),
          borderColor: colors,
          borderWidth: type === 'doughnut' ? 0 : 2,
          fill: type === 'line' ? false : true
        }]
      };
    }
    
    function getChartOptions() {
      const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: type === 'doughnut' ? 'right' : 'top',
            labels: {
              color: 'rgb(156, 163, 175)', // gray-400
              font: {
                size: 12
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: 'white',
            bodyColor: 'white',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1
          }
        }
      };
      
      if (type === 'bar') {
        return {
          ...baseOptions,
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(156, 163, 175, 0.1)'
              },
              ticks: {
                color: 'rgb(156, 163, 175)'
              }
            },
            x: {
              grid: {
                color: 'rgba(156, 163, 175, 0.1)'
              },
              ticks: {
                color: 'rgb(156, 163, 175)'
              }
            }
          }
        };
      }
      
      if (type === 'line') {
        return {
          ...baseOptions,
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(156, 163, 175, 0.1)'
              },
              ticks: {
                color: 'rgb(156, 163, 175)'
              }
            },
            x: {
              grid: {
                color: 'rgba(156, 163, 175, 0.1)'
              },
              ticks: {
                color: 'rgb(156, 163, 175)'
              }
            }
          }
        };
      }
      
      return baseOptions;
    }
    
    function getDefaultColor(): string {
      const colors = [
        '#3B82F6', '#EF4444', '#10B981', '#F59E0B',
        '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    }
  </script>
  
  <div class="chart-container" style="height: {height}px; position: relative;">
    <canvas bind:this={canvas}></canvas>
  </div>
  
  <style>
    .chart-container {
      width: 100%;
    }
  </style>
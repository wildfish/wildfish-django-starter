var {{cookiecutter.model_name}}Grid = React.createClass({
    getInitialState: function(){
        return {
            results: [],
            maxPages: 0,
            externalResultsPerPage: 5,
            externalSortSortColumn: null,
            externalSortAscending: true,
            currentPage: 0
        };
    },
    updateResults: function(){
        var _this = this;
        $.get(this.props.apiUrl + '?page=' + (this.state.currentPage + 1) + '&page_size=' + this.state.externalResultsPerPage).success(function(data) {
            _this.setState({
                results: data.results,
                maxPages: Math.ceil(data.count / _this.state.externalResultsPerPage)
            });
        });
    },
    componentDidMount: function(){
        this.updateResults();
    },
    //what page is currently viewed
    setPage: function(index){
        this.setState({currentPage: index}, function(){this.updateResults();});
    },
    //this will handle how the data is sorted
    sortData: function(sort, sortAscending, data){
    },
    //this changes whether data is sorted in ascending or descending order
    changeSort: function(sort, sortAscending){
    },
    //this method handles the filtering of the data
    setFilter: function(filter){
    },
    //this method handles determining the page size
    setPageSize: function(size){
        this.setState({externalResultsPerPage: size}, function(){this.updateResults();});
    },
    render: function(){
        return <Griddle
            columns={['name']}
            useExternal={true}
            externalSetPage={this.setPage}
            externalChangeSort={this.changeSort}
            externalSetFilter={this.setFilter}
            externalSetPageSize={this.setPageSize}
            externalMaxPage={this.state.maxPages}
            externalCurrentPage={this.state.currentPage}
            results={this.state.results}
            resultsPerPage={this.state.externalResultsPerPage}
            externalSortColumn={this.state.externalSortColumn}
            externalSortAscending={this.state.externalSortAscending}
            showSettings={true}
        />
    }
});
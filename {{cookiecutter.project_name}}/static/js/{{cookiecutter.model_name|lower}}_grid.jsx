var {{cookiecutter.model_name}}Grid = React.createClass({
    getInitialState: function(){
        return {
            results: [],
            maxPages: 0,
            externalResultsPerPage: 20,
            externalSortSortColumn: null,
            externalSortAscending: true,
            currentPage: 1
        };
    },
    componentDidMount: function(){
        _this = this
        $.get(this.props.apiUrl).success(function(data) {
            _this.setState({
                results: data
            });
        });
    },
    //what page is currently viewed
    setPage: function(index){
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
        />
    }
});